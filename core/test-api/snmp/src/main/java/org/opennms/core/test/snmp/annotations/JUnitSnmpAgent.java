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



package org.opennms.core.test.snmp.annotations;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * <p>JUnitSnmpAgent class.</p>
 *
 * @author brozow
 * @version $Id: $
 */

@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD,ElementType.TYPE})
public @interface JUnitSnmpAgent {

    String resource() default "classpath:snmpwalk.properties";
    String host() default "";
    /**
     * This value should match the port value configured in the unit test spring context object
     * {@link ProxySnmpAgentConfigFactory}
     */
    int port() default 9161;
    /**
     * If set to true, use the MockSnmpStrategy instead of the MockSnmpAgent.  Note that if
     * this annotation is inside a {@link JUnitSnmpAgents} annotation, the "useMockSnmpStrategy" 
     * property there will override this.
     * @return whether to use the MockSnmpStrategy
     */
    boolean useMockSnmpStrategy() default false;
}
