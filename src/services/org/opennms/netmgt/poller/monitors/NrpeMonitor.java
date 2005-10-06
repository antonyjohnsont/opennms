//This file is part of the OpenNMS(R) Application.
//
// OpenNMS(R) is Copyright (C) 2002-2003 The OpenNMS Group, Inc. All rights reserved.
// OpenNMS(R) is a derivative work, containing both original code, included code and modified
// code that was published under the GNU General Public License. Copyrights for modified
// and included code are below.
//
// OpenNMS(R) is a registered trademark of The OpenNMS Group, Inc.
//
// Modifications:
//
// 2005 Aug 04: Create NrpeMonitor based on TcpMonitor.
//
// Original code base Copyright (C) 1999-2001 Oculan Corp. All rights reserved.
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
//
// For more information contact:
//      OpenNMS Licensing <license@opennms.org>
//      http://www.opennms.org/
//      http://www.opennms.com/
//
// Tab Size = 8
//

package org.opennms.netmgt.poller.monitors;

import java.io.IOException;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.net.ConnectException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.NoRouteToHostException;
import java.net.Socket;
import java.util.Map;

import org.apache.log4j.Category;
import org.apache.log4j.Priority;
import org.opennms.core.utils.ThreadCategory;
import org.opennms.netmgt.poller.MonitoredService;
import org.opennms.netmgt.poller.NetworkInterface;
import org.opennms.netmgt.poller.NetworkInterfaceNotSupportedException;
import org.opennms.netmgt.poller.nrpe.CheckNrpe;
import org.opennms.netmgt.poller.nrpe.NrpeException;
import org.opennms.netmgt.poller.nrpe.NrpePacket;
import org.opennms.netmgt.utils.ParameterMap;

/**
 * This class is designed to be used by the service poller framework to test the
 * availability of a generic TCP service on remote interfaces. The class
 * implements the ServiceMonitor interface that allows it to be used along with
 * other plug-ins by the service poller framework.
 * 
 * @author <A HREF="mailto:dgregor@interhack.com">DJ Gregor</A>
 * @author <A HREF="mailto:tarus@opennms.org">Tarus Balog </A>
 * @author <A HREF="mike@opennms.org">Mike </A>
 * @author Weave
 * @author <A HREF="http://www.opennms.org/">OpenNMS </A>
 * 
 */
final public class NrpeMonitor extends IPv4LatencyMonitor {

    /**
     * Default port.
     */
    //Commented out because it is not currently used in this monitor
    //private static final int DEFAULT_PORT = -1;

    /**
     * Default retries.
     */
    private static final int DEFAULT_RETRY = 0;

    /**
     * Default timeout. Specifies how long (in milliseconds) to block waiting
     * for data from the monitored interface.
     */
    private static final int DEFAULT_TIMEOUT = 3000; // 3 second timeout on
                                                        // read()

    /**
     * Poll the specified address for service availability.
     * 
     * During the poll an attempt is made to connect on the specified port. If
     * the connection request is successful, the banner line generated by the
     * interface is parsed and if the banner text indicates that we are talking
     * to Provided that the interface's response is valid we set the service
     * status to SERVICE_AVAILABLE and return.
     * @param parameters
     *            The package parameters (timeout, retry, etc...) to be used for
     *            this poll.
     * @param iface
     *            The network interface to test the service on.
     * 
     * @return The availibility of the interface and if a transition event
     *         should be supressed.
     * 
     * @throws java.lang.RuntimeException
     *             Thrown if the interface experiences errors during the poll.
     */
    public int checkStatus(MonitoredService svc, Map parameters, org.opennms.netmgt.config.poller.Package pkg) {
        NetworkInterface iface = svc.getNetInterface();

        //
        // Process parameters
        //
        Category log = ThreadCategory.getInstance(getClass());

        //
        // Get interface address from NetworkInterface
        //
        if (iface.getType() != NetworkInterface.TYPE_IPV4)
            throw new NetworkInterfaceNotSupportedException("Unsupported interface type, only TYPE_IPV4 currently supported");

        String command = ParameterMap.getKeyedString(parameters, "command", NrpePacket.HELLO_COMMAND);
        int port = ParameterMap.getKeyedInteger(parameters, "port", CheckNrpe.DEFAULT_PORT);
        int padding = ParameterMap.getKeyedInteger(parameters, "padding", NrpePacket.DEFAULT_PADDING);
        int retry = ParameterMap.getKeyedInteger(parameters, "retry", DEFAULT_RETRY);
        int timeout = ParameterMap.getKeyedInteger(parameters, "timeout", DEFAULT_TIMEOUT);
        String rrdPath = ParameterMap.getKeyedString(parameters, "rrd-repository", null);
        String dsName = ParameterMap.getKeyedString(parameters, "ds-name", null);

        if (rrdPath == null) {
            log.info("poll: RRD repository not specified in parameters, latency data will not be stored.");
        }
        if (dsName == null) {
            dsName = DEFAULT_DSNAME;
        }

		/*
        // Port
        //
        int port = ParameterMap.getKeyedInteger(parameters, "port", DEFAULT_PORT);
        if (port == DEFAULT_PORT) {
            throw new RuntimeException("TcpMonitor: required parameter 'port' is not present in supplied properties.");
        }
        */

        // BannerMatch
        //
        //Commented out because it is not currently referenced in this monitor
        //String strBannerMatch = (String) parameters.get("banner");

        // Get the address instance.
        //
        InetAddress ipv4Addr = (InetAddress) iface.getAddress();

        if (log.isDebugEnabled())
            log.debug("poll: address = " + ipv4Addr.getHostAddress() + ", port = " + port + ", timeout = " + timeout + ", retry = " + retry);

        // Give it a whirl
        //
        int serviceStatus = SERVICE_UNAVAILABLE;
        long responseTime = -1;

        for (int attempts = 0; attempts <= retry && serviceStatus != SERVICE_AVAILABLE; attempts++) {
            Socket socket = null;
            try {
                //
                // create a connected socket
                //
                long sentTime = System.currentTimeMillis();

                socket = new Socket();
                socket.connect(new InetSocketAddress(ipv4Addr, port), timeout);
                socket.setSoTimeout(timeout);
                log.debug("TcpMonitor: connected to host: " + ipv4Addr + " on port: " + port);

                // We're connected, so upgrade status to unresponsive
                serviceStatus = SERVICE_UNRESPONSIVE;

				NrpePacket p = new NrpePacket(NrpePacket.QUERY_PACKET, (short) 0,
						command);
				byte[] b = p.buildPacket(padding);
				OutputStream o = socket.getOutputStream();
				o.write(b);

				/*
                if (strBannerMatch == null || strBannerMatch.length() == 0 || strBannerMatch.equals("*")) {

				if (true) {
                    serviceStatus = SERVICE_AVAILABLE;
                    // Store response time in RRD
                    if (responseTime >= 0 && rrdPath != null) {
                        try {
                            this.updateRRD(rrdPath, ipv4Addr, dsName, responseTime, pkg);
                        } catch (RuntimeException rex) {
                            log.debug("There was a problem writing the RRD:" + rex);
                        }
                    }
                    break;
                }

                BufferedReader rdr = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                //
                // Tokenize the Banner Line, and check the first
                // line for a valid return.
                //
                String response = rdr.readLine();
                responseTime = System.currentTimeMillis() - sentTime;

                if (response == null)
                    continue;
                if (log.isDebugEnabled()) {
                    log.debug("poll: banner = " + response);
                    log.debug("poll: responseTime= " + responseTime + "ms");
                }

                if (response.indexOf(strBannerMatch) > -1) {
                */

				NrpePacket response = NrpePacket.receivePacket(socket.getInputStream(), padding);
                responseTime = System.currentTimeMillis() - sentTime;
				if (response.getResultCode() == 0) {
                    serviceStatus = SERVICE_AVAILABLE;
                    // Store response time in RRD
                    if (responseTime >= 0 && rrdPath != null) {
                        try {
                            this.updateRRD(rrdPath, ipv4Addr, dsName, responseTime, pkg);
                        } catch (RuntimeException rex) {
                            log.debug("There was a problem writing the RRD:" + rex);
                        }
                    }
                } else {
                    serviceStatus = SERVICE_UNAVAILABLE;
                }
            } catch (NoRouteToHostException e) {
                e.fillInStackTrace();
                if (log.isEnabledFor(Priority.WARN))
                    log.warn("poll: No route to host exception for address " + ipv4Addr.getHostAddress(), e);
                break; // Break out of for(;;)
            } catch (InterruptedIOException e) {
                log.debug("TcpMonitor: did not connect to host within timeout: " + timeout + " attempt: " + attempts);
            } catch (ConnectException e) {
                // Connection refused. Continue to retry.
                //
                e.fillInStackTrace();
                if (log.isDebugEnabled())
                    log.debug("poll: Connection exception for address: " + ipv4Addr, e);
            } catch (NrpeException e) {
                // Ignore
                e.fillInStackTrace();
                if (log.isDebugEnabled())
                    log.debug("poll: NrpeException while polling address: " + ipv4Addr, e);
            } catch (IOException e) {
                // Ignore
                e.fillInStackTrace();
                if (log.isDebugEnabled())
                    log.debug("poll: IOException while polling address: " + ipv4Addr, e);
            } finally {
                try {
                    // Close the socket
                    if (socket != null)
                        socket.close();
                } catch (IOException e) {
                    e.fillInStackTrace();
                    if (log.isDebugEnabled())
                        log.debug("poll: Error closing socket.", e);
                }
            }
        }

        //
        // return the status of the service
        //
        return serviceStatus;
    }

}
