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

package org.opennms.netmgt.syslogd;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.TimeZone;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.opennms.core.utils.LogUtils;

public class SyslogNGParser extends SyslogParser {
    //                                                                <PRI>        IDENT     TIMESTAMP                    HOST   PROCESS/ID                          MESSAGE
    private static final Pattern m_syslogNGPattern = Pattern.compile("^<(\\d{1,3})>(\\S+?):? (\\d\\d\\d\\d-\\d\\d-\\d\\d) (\\S+) (?:(\\S+?)(?:\\[(\\d+)\\])?: ){0,1}(\\S.*?)$", Pattern.MULTILINE);
    
    protected SyslogNGParser(final String text) {
        super(text);
    }

    public static SyslogParser getParser(final String text) {
        return new SyslogNGParser(text);
    }

    protected Pattern getPattern() {
        return m_syslogNGPattern;
    }

    public SyslogMessage parse() throws SyslogParserException {
        if (!this.find()) {
            if (traceEnabled()) {
                LogUtils.tracef(this, "'%s' did not match '%s'", m_syslogNGPattern, getText());
            }
            return null;
        }

        final Matcher matcher = getMatcher();
        final SyslogMessage message = new SyslogMessage();
        try {
            int priorityField = Integer.parseInt(matcher.group(1));
            message.setFacility(getFacility(priorityField));
            message.setSeverity(getSeverity(priorityField));
        } catch (final NumberFormatException e) {
            LogUtils.debugf(this, e, "Unable to parse priority field '%s'", matcher.group(1));
        }
        message.setMessageID(matcher.group(2));
        try {
            final DateFormat df = new SimpleDateFormat("yyyy-MM-dd");
            df.setTimeZone(TimeZone.getTimeZone("UTC"));
            message.setDate(df.parse(matcher.group(3)));
        } catch (final Exception e) {
            LogUtils.debugf(this, e, "Unable to parse date '%s'", matcher.group(3));
        }

        message.setHostName(matcher.group(4));
        message.setProcessName(matcher.group(5));
        if (matcher.group(6) != null) {
            try {
                final Integer pid = Integer.parseInt(matcher.group(6));
                message.setProcessId(pid);
            } catch (final NumberFormatException nfe) {
                LogUtils.debugf(this, nfe, "Unable to parse '%s' as a process ID.", matcher.group(6));
            }
        }
        message.setMessage(matcher.group(7));

        return message;
    }
}
