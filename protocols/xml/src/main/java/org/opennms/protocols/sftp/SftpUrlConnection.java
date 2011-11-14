/*******************************************************************************
 * This file is part of OpenNMS(R).
 *
 * Copyright (C) 2010-2011 The OpenNMS Group, Inc.
 * OpenNMS(R) is Copyright (C) 1999-2011 The OpenNMS Group, Inc.
 *
 * OpenNMS(R) is a registered trademark of The OpenNMS Group, Inc.
 *
 * OpenNMS(R) is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published
 * by the Free Software Foundation, either version 3 of the License,
 * or (at your option) any later version.
 *
 * OpenNMS(R) is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with OpenNMS(R).  If not, see:
 *      http://www.gnu.org/licenses/
 *
 * For more information contact:
 *     OpenNMS(R) Licensing <license@opennms.org>
 *     http://www.opennms.org/
 *     http://www.opennms.com/
 *******************************************************************************/
package org.opennms.protocols.sftp;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;

import org.opennms.core.utils.ThreadCategory;

import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;

/**
 * The class for managing SFTP URL Connection.
 * <p>The default connection timeout is 30 seconds.</p>
 * 
 * @author <a href="mailto:agalue@opennms.org">Alejandro Galue</a>
 */
public class SftpUrlConnection extends URLConnection {

    /** The Constant default timeout in milliseconds. */
    public static final int DEFAULT_TIMEOUT = 30000;

    /** The URL. */
    protected URL m_url;

    /** The SSH session. */
    protected Session m_session; 

    /** The SFTP channel. */
    protected ChannelSftp m_channel;

    /** The connection flag, true when the connection has been started. */
    protected boolean m_connected = false;

    /**
     * Instantiates a new SFTP URL connection.
     *
     * @param url the URL
     */
    protected SftpUrlConnection(URL url) {
        super(url);
        m_url = url;
    }

    /* (non-Javadoc)
     * @see java.net.URLConnection#connect()
     */
    @Override
    public void connect() throws IOException {
        if (m_connected) {
            return;
        }
        m_connected = true;
        if (m_url.getUserInfo() == null) {
            throw new IOException("User credentials required.");
        }
        String[] userInfo = m_url.getUserInfo().split(":");
        JSch jsch = new JSch();
        try {
            int port = m_url.getPort() > 0 ? m_url.getPort() : m_url.getDefaultPort();
            m_session = jsch.getSession(userInfo[0], m_url.getHost(), port);
            if (userInfo.length > 1) {
                m_session.setPassword(userInfo[1]);
            }
            java.util.Properties config = new java.util.Properties();
            config.put("StrictHostKeyChecking", "no");
            m_session.setConfig(config);
            m_session.setTimeout(DEFAULT_TIMEOUT);
            m_session.connect();
            m_channel = (ChannelSftp) m_session.openChannel("sftp");
            m_channel.connect();
        } catch (JSchException e) {
            disconnect();
            throw new IOException("Can't connect using " + m_url + " because " + e.getMessage());
        }
    }

    /**
     * Disconnect.
     *
     * @throws IOException Signals that an I/O exception has occurred.
     */
    public void disconnect() throws IOException {
        if (m_channel != null)
            m_channel.disconnect();
        if (m_session != null)
            m_session.disconnect();
    }

    /**
     * Gets the channel.
     *
     * @return the channel
     */
    public ChannelSftp getChannel() {
        return m_channel;
    }

    /* (non-Javadoc)
     * @see java.net.URLConnection#getInputStream()
     */
    @Override
    public InputStream getInputStream() throws IOException {
        try {
            connect();
            return m_channel.get(getPath());
        } catch (Exception e) {
            throw new IOException("Can't retrieve " + m_url.getPath() + " from " + m_url.getHost() + " because " + e.getMessage());
        }
    }

    /**
     * Gets the path.
     *
     * @return the path
     * @throws SftpUrlException the SFTP URL exception
     */
    protected String getPath() throws SftpUrlException {
        return m_url.getPath();
    }

    /**
     * Log.
     *
     * @return the thread category
     */
    protected ThreadCategory log() {
        return ThreadCategory.getInstance(getClass());
    }

}