<!--

//
// This file is part of the OpenNMS(R) Application.
//
// OpenNMS(R) is Copyright (C) 2002-2003 Blast Internet Services, Inc.  All rights reserved.
// OpenNMS(R) is a derivative work, containing both original code, included code and modified
// code that was published under the GNU General Public License. Copyrights for modified 
// and included code are below.
//
// OpenNMS(R) is a registered trademark of Blast Internet Services, Inc.
//
// Modifications:
//
// 2003 Feb 07: Fixed URLEncoder issues.
// 2002 Nov 26: Fixed breadcrumbs issue.
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

-->

<%@page language="java" contentType = "text/html" session = "true"  import="org.opennms.netmgt.config.*, java.util.*,java.text.*,org.opennms.netmgt.config.groups.*"%>
<%
	Group group = null;
  	String groupName = request.getParameter("groupName");
	try
  	{
		GroupFactory.init();
		GroupFactory groupFactory = GroupFactory.getInstance();
      		group = groupFactory.getGroup(groupName);
  	}
	catch (Exception e)
  	{
      		throw new ServletException("Could not find group " + groupName + " in group factory.", e);
  	}

%>
<html>
<head>
<title>Group Detail | User Admin | OpenNMS Web Console</title>
<base HREF="<%=org.opennms.web.Util.calculateUrlBase( request )%>" />
<link rel="stylesheet" type="text/css" href="includes/styles.css" />
</head>

<body marginwidth="0" marginheight="0" LEFTMARGIN="0" RIGHTMARGIN="0" TOPMARGIN="0">

<% String breadcrumb1 = "<a href='admin/index.jsp'>Admin</a>"; %>
<% String breadcrumb2 = "<a href='admin/userGroupView/index.jsp'>Users and Groups</a>"; %>
<% String breadcrumb3 = "<a href='admin/userGroupView/groups/list.jsp'>Group List</a>"; %>
<% String breadcrumb4 = "Group Detail"; %>
<jsp:include page="/includes/header.jsp" flush="false" >
  <jsp:param name="title" value="Group Detail" />
  <jsp:param name="breadcrumb" value="<%=breadcrumb1%>" />
  <jsp:param name="breadcrumb" value="<%=breadcrumb2%>" />
  <jsp:param name="breadcrumb" value="<%=breadcrumb3%>" />
  <jsp:param name="breadcrumb" value="<%=breadcrumb4%>" />
</jsp:include>

<br>

<table width="100%" border="0" cellspacing="0" cellpadding="2" >
  <tr>
    <td>&nbsp;</td>

    <td>
    <table width="100%" border="0" cellspacing="0" cellpadding="2" >
      <tr>
        <td>
          <h2>Details for Group: <%=group.getName()%></h2>
          <table width="100%" border="0" cellspacing="0" cellpadding="2">
            <tr>
              <td width="10%" valign="top">
                <b>Comments:</b>
              </td>
              <td width="90%" valign="top">
                <%=group.getComments()%>
              </td>
            </tr>
          </table>
        </td>
      </tr>
      <br>
      <tr>
        <td>
          <table width="100%" border="0" cellspacing="0" cellpadding="2" >
            <tr>
              <td>
                <b>Assigned Users:</b>
                <% Collection users = group.getUserCollection();
                if (users.size() < 1)
                { %>
                  <table width="50%" border="0" cellspacing="0" cellpadding="2" >
                    <tr>
                      <td>
                        No users belong to this group.
                      </td>
                    </tr>
                  </table>
                <% }
                else { %>
                  <table width="50%" border="1" cellspacing="0" cellpadding="2" >
                    <% 	Iterator usersIter = (Iterator)users.iterator(); 
			while (usersIter != null && usersIter.hasNext()) { %>
                      <tr>
                        <td>
                          <%=(String)usersIter.next()%>
                        </td>
                      </tr>
                    <% } %>
                  </table>
                <% } %>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
    </td>

    <td>&nbsp;</td>
  </tr>
</table>

<br>

<jsp:include page="/includes/footer.jsp" flush="false" >
</jsp:include>
</body>
</html>
