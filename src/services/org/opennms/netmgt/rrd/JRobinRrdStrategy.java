//
// This file is part of the OpenNMS(R) Application.
//
// OpenNMS(R) is Copyright (C) 2002-2004 Blast Internet Services, Inc.  All rights reserved.
// OpenNMS(R) is a derivative work, containing both original code, included code and modified
// code that was published under the GNU General Public License. Copyrights for modified 
// and included code are below.
//
// OpenNMS(R) is a registered trademark of Blast Internet Services, Inc.
//
// Modifications:
//
// Jul 8, 2004: Created this file.
//
// Original code base Copyright (C) 1999-2001 Oculan Corp.  All rights reserved.
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.                                                            
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
//       
// For more information contact: 
//      OpenNMS Licensing       <license@opennms.org>
//      http://www.opennms.org/
//      http://www.blast.com/
//
// Tab Size = 8
//

package org.opennms.netmgt.rrd;

import java.awt.Color;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import org.apache.log4j.Category;
import org.jrobin.core.FetchData;
import org.jrobin.core.RrdDb;
import org.jrobin.core.RrdDef;
import org.jrobin.core.RrdException;
import org.jrobin.core.Sample;
import org.jrobin.graph.RrdGraph;
import org.jrobin.graph.RrdGraphDef;
import org.opennms.core.utils.ThreadCategory;

/**
 * Provides a JRobin based implementation of RrdStrategy. It uses JRobin 1.4 in
 * FILE mode (NIO is too memory consuming for the large number of files that we
 * open)
 */
public class JRobinRrdStrategy implements RrdStrategy {

    /**
     * Closes the JRobin RrdDb.
     */
    public void closeFile(Object rrdFile) throws Exception {
        ((RrdDb) rrdFile).close();
    }

    /**
     * Creates and returns a RrdDef represented by the parameters.
     */
    public Object createDefinition(String creator, String directory, String dsName, int step, String dsType, int dsHeartbeat, String dsMin, String dsMax, List rraList) throws Exception {

        File f = new File(directory);
        f.mkdirs();

        String fileName = directory + File.separator + dsName + ".rrd";

        RrdDef def = new RrdDef(fileName);

        //def.setStartTime(System.currentTimeMillis()/1000L - 2592000L);
        def.setStartTime(1000);
        def.setStep(step);

        double min = (dsMin == null || "U".equals(dsMin) ? Double.NaN : Double.parseDouble(dsMin));
        double max = (dsMax == null || "U".equals(dsMax) ? Double.NaN : Double.parseDouble(dsMax));
        def.addDatasource(dsName, dsType, dsHeartbeat, min, max);

        for (Iterator it = rraList.iterator(); it.hasNext();) {
            String rra = (String) it.next();
            def.addArchive(rra);
        }

        return def;

    }

    /**
     * Creates the JRobin RrdDb from the def by opening the file and then
     * closing. TODO: Change the interface here to create the file and return it
     * opened.
     */
    public void createFile(Object rrdDef) throws Exception {
        RrdDb rrd = new RrdDb((RrdDef) rrdDef);
        rrd.close();
    }

    /**
     * Opens the JRobin RrdDb by name and returns it.
     */
    public Object openFile(String fileName) throws Exception {
        RrdDb rrd = new RrdDb(fileName);
        return rrd;
    }

    /**
     * Creates a sample from the JRobin RrdDb and passes in the data provided.
     */
    public void updateFile(Object rrdFile, String data) throws Exception {
        Sample sample = ((RrdDb) rrdFile).createSample();
        sample.setAndUpdate(data);
    }

    /**
     * Initialized the RrdDb to use the FILE factory because the NIO factory
     * uses too much memory for our implementation.
     */
    public void initialize() throws Exception {
        RrdDb.setDefaultFactory("FILE");
    }

    /* (non-Javadoc)
     * @see org.opennms.netmgt.rrd.RrdStrategy#graphicsInitialize()
     */
    public void graphicsInitialize() throws Exception {
        initialize();
    }
    /**
     * Fetch the last value from the JRobin RrdDb file.
     */
    public Double fetchLastValue(String fileName, int interval) throws NumberFormatException, org.opennms.netmgt.rrd.RrdException {
        try {
            long now = System.currentTimeMillis();
            long collectTime = (now - (now % interval)) / 1000L;
            RrdDb rrd = new RrdDb(fileName);
            FetchData data = rrd.createFetchRequest("AVERAGE", collectTime, collectTime).fetchData();
            double[] vals = data.getValues(0);
            if (vals.length > 0) {
                return new Double(vals[vals.length - 1]);
            }
            return null;
        } catch (IOException e) {
            throw new org.opennms.netmgt.rrd.RrdException("Exception occurred fetching data from " + fileName, e);
        } catch (RrdException e) {
            throw new org.opennms.netmgt.rrd.RrdException("Exception occurred fetching data from " + fileName, e);
        }
    }

    private Color getColor(String colorValue) {
        int colorVal = Integer.parseInt(colorValue, 16);
        return new Color(colorVal);
    }

    private String[] tokenize(String line, String delims) {
        Category log = ThreadCategory.getInstance(getClass());
        List tokenList = new LinkedList();

        StringBuffer currToken = new StringBuffer();
        boolean quoting = false;
        boolean escaping = false;
        boolean debugTokens = false;

        if (debugTokens)
            log.debug("tokenize: line=" + line + " delims=" + delims);
        for (int i = 0; i < line.length(); i++) {
            char ch = line.charAt(i);
            if (debugTokens)
                log.debug("tokenize: checking char: " + ch);
            if (escaping) {
                if (ch == 'n') {
                    currToken.append('\n');
                } else if (ch == 'r') {
                    currToken.append('\r');
                } else if (ch == 't') {
                    currToken.append('\t');
                } else {
                    currToken.append(ch);
                }
                escaping = false;
                if (debugTokens)
                    log.debug("tokenize: escaped. appended to " + currToken);
            } else if (ch == '\\') {
                if (debugTokens)
                    log.debug("tokenize: found a backslash... escaping currToken = " + currToken);
                escaping = true;
            } else if (ch == '\"') {
                if (quoting) {
                    if (debugTokens)
                        log.debug("tokenize: found a quote ending quotation currToken = " + currToken);
                    quoting = false;
                } else {
                    if (debugTokens)
                        log.debug("tokenize: found a quote beginning quotation  currToke =" + currToken);
                    quoting = true;
                }
            } else if (!quoting && delims.indexOf(ch) >= 0) {
                if (debugTokens)
                    log.debug("tokenize: found a token: " + ch + " ending token [" + currToken + "] and starting a new one");
                tokenList.add(currToken.toString());
                currToken = new StringBuffer();
            } else {
                if (debugTokens)
                    log.debug("tokenize: appending " + ch + " to token: " + currToken);
                currToken.append(ch);
            }

        }

        if (escaping || quoting) {
            if (debugTokens)
                log.debug("tokenize: ended string but escaping = " + escaping + " and quoting = " + quoting);
            throw new IllegalArgumentException("unable to tokenize string " + line + " with token chars " + delims);
        }

        if (debugTokens)
            log.debug("tokenize: reached end of string.  completing token " + currToken);
        tokenList.add(currToken.toString());

        return (String[]) tokenList.toArray(new String[tokenList.size()]);
    }

    /**
     * This constructs a graphDef by parsing the rrdtool style command and using
     * the values to create the JRobin graphDef. It does not understand the 'AT
     * style' time arguments however. Also there may be some rrdtool parameters
     * that it does not understand. These will be ignored. The graphDef will be
     * used to construct an RrdGraph and a PNG image will be created. An input
     * stream returning the bytes of the PNG image is returned.
     */
    public InputStream createGraph(String command, File workDir) throws IOException, org.opennms.netmgt.rrd.RrdException {
        Category log = ThreadCategory.getInstance(getClass());
        try {
            InputStream tempIn = null;
            String[] commandArray = tokenize(command, " \t");

            RrdGraphDef graphDef = new RrdGraphDef();
            long start = 0;
            long end = 0;
            for (int i = 0; i < commandArray.length; i++) {
                String arg = commandArray[i];
                if (arg.startsWith("--start=")) {
                    start = Long.parseLong(arg.substring("--start=".length()));
                    log.debug("JRobin start time: " + start);
                } else if (arg.equals("--start")) {
                    if (i + 1 < commandArray.length) {
                        start = Long.parseLong(commandArray[++i]);
                        log.debug("JRobin start time: " + start);
                    } else {
                        throw new IllegalArgumentException("--start must be followed by a start time");
                    }
                } else if (arg.startsWith("--end=")) {
                    end = Long.parseLong(arg.substring("--end=".length()));
                    log.debug("JRobin end time: " + end);
                } else if (arg.equals("--end")) {
                    if (i + 1 < commandArray.length) {
                        end = Long.parseLong(commandArray[++i]);
                        log.debug("JRobin end time: " + start);
                    } else {
                        throw new IllegalArgumentException("--end must be followed by an end time");
                    }
                } else if (arg.startsWith("--title=")) {
                    String[] title = tokenize(arg, "=");
                    graphDef.setTitle(title[1]);
                } else if (arg.equals("--title")) {
                    if (i + 1 < commandArray.length) {
                        graphDef.setTitle(commandArray[++i]);
                    } else {
                        throw new IllegalArgumentException("--title must be followed by a title");
                    }
                } else if (arg.startsWith("DEF:")) {
                    String definition = arg.substring("DEF:".length());
                    String[] def = tokenize(definition, ":");
                    String[] ds = tokenize(def[0], "=");
                    File dsFile = new File(workDir, ds[1]);
                    graphDef.datasource(ds[0], dsFile.getAbsolutePath(), def[1], def[2]);
                } else if (arg.startsWith("CDEF:")) {
                    String definition = arg.substring("CDEF:".length());
                    String[] cdef = tokenize(definition, "=");
                    graphDef.datasource(cdef[0], cdef[1]);
                } else if (arg.startsWith("LINE1:")) {
                    String definition = arg.substring("LINE1:".length());
                    String[] line1 = tokenize(definition, ":");
                    String[] color = tokenize(line1[0], "#");
                    graphDef.line(color[0], getColor(color[1]), line1[1]);
                } else if (arg.startsWith("LINE2:")) {
                    String definition = arg.substring("LINE2:".length());
                    String[] line2 = tokenize(definition, ":");
                    String[] color = tokenize(line2[0], "#");
                    graphDef.line(color[0], getColor(color[1]), line2[1], 2);

                } else if (arg.startsWith("LINE3:")) {
                    String definition = arg.substring("LINE3:".length());
                    String[] line3 = tokenize(definition, ":");
                    String[] color = tokenize(line3[0], "#");
                    graphDef.line(color[0], getColor(color[1]), line3[1], 3);

                } else if (arg.startsWith("GPRINT:")) {
                    String definition = arg.substring("GPRINT:".length());
                    String gprint[] = tokenize(definition, ":");
                    String format = gprint[2];
                    format = format.replaceAll("%(\\d*\\.\\d*)lf", "@$1");
                    format = format.replaceAll("%s", "@s");
                    log.debug("gprint: oldformat = " + gprint[2] + " newformat = " + format);
                    graphDef.gprint(gprint[0], gprint[1], format);

                } else if (arg.startsWith("AREA:")) {
                    String definition = arg.substring("AREA:".length());
                    String area[] = tokenize(definition, ":");
                    String[] color = tokenize(area[0], "#");
                    graphDef.area(color[0], getColor(color[1]), area[1]);

                } else if (arg.startsWith("STACK:")) {
                    String definition = arg.substring("STACK:".length());
                    String stack[] = tokenize(definition, ":");
                    String[] color = tokenize(stack[0], "#");
                    graphDef.stack(color[0], getColor(color[1]), stack[1]);
                } else {
                    log.warn("JRobin: Unrecognized graph argument: " + arg);
                }
            }
            graphDef.setTimePeriod(start, end);

            log.debug("JRobin Finished tokenizing checking: start time: " + start + "; end time: " + end);

            RrdGraph graph = new RrdGraph(graphDef, false);

            byte[] bytes = graph.getPNGBytes();

            tempIn = new ByteArrayInputStream(bytes);

            return tempIn;
        } catch (Exception e) {
            log.error("JRobin:exception occurred creating graph", e);
            throw new org.opennms.netmgt.rrd.RrdException("An exception occurred creating the graph.", e);
        }
    }

    /**
     * This implementation does not track and stats.
     */
    public String getStats() {
        return "";
    }
}