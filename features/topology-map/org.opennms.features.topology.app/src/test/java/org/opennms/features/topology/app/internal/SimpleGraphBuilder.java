package org.opennms.features.topology.app.internal;

import org.opennms.features.topology.api.SimpleConnector;
import org.opennms.features.topology.api.SimpleEdge;
import org.opennms.features.topology.api.topo.AbstractVertexRef;
import org.opennms.features.topology.api.topo.GraphProvider;
import org.opennms.features.topology.api.topo.Vertex;
import org.opennms.features.topology.api.topo.VertexRef;

public class SimpleGraphBuilder {

	private final GraphProvider m_graphProvider;
	private SimpleVertex m_currentVertex;
	private SimpleEdge m_currentEdge;
	
	public SimpleGraphBuilder(String namespace) {
		m_graphProvider = new SimpleTopologyProvider();
	}
	
	public SimpleGraphBuilder vertex(String id) {
		m_currentVertex = new SimpleVertex(ns(), id);
		m_graphProvider.addVertices(m_currentVertex);
		return this;
	}
	
	public SimpleGraphBuilder parent(String parentId) {
		Vertex parent = m_graphProvider.getVertex(ns(), parentId);
		m_graphProvider.setParent(m_currentVertex, parent);
		return this;
	}
	
	public SimpleGraphBuilder vLabel(String label) {
		m_currentVertex.setLabel(label);
		return this;
	}
	
	public SimpleGraphBuilder vTooltip(String tooltipText) {
		m_currentVertex.setTooltipText(tooltipText);
		return this;
	}
	
	public SimpleGraphBuilder vIconKey(String iconKey) {
		m_currentVertex.setIconKey(iconKey);
		return this;
	}
	
	public SimpleGraphBuilder vStyleName(String styleName) {
		m_currentVertex.setStyleName(styleName);
		return this;
	}
	
	public SimpleGraphBuilder edge(String id, String srcId, String tgtId) {
		
		VertexRef srcVertex = m_graphProvider.getVertex(ns(), srcId);
		if (srcVertex == null) {
			srcVertex = new AbstractVertexRef(ns(), srcId);
		}
		
		VertexRef tgtVertex = m_graphProvider.getVertex(ns(), tgtId);
		if (tgtVertex == null) {
			tgtVertex = new AbstractVertexRef(ns(), tgtId);
		}
		
		
		SimpleConnector source = new SimpleConnector(ns(), srcId+"-"+id+"-connector", srcVertex);
		SimpleConnector target = new SimpleConnector(ns(), tgtId+"-"+id+"-connector", tgtVertex);
		
		m_currentEdge = new SimpleEdge(ns(), id, source, target);
		
		source.setEdge(m_currentEdge);
		target.setEdge(m_currentEdge);
		
		m_graphProvider.addEdges(m_currentEdge);
		
		return this;
	}
	
	public SimpleGraphBuilder eLabel(String label) {
		m_currentEdge.setLabel(label);
		return this;
	}
	
	public SimpleGraphBuilder eTooltip(String tooltipText) {
		m_currentEdge.setTooltipText(tooltipText);
		return this;
	}
	
	public SimpleGraphBuilder eStyleName(String styleName) {
		m_currentEdge.setStyleName(styleName);
		return this;
	}
	
	public GraphProvider get() {
		return m_graphProvider;
	}

	private String ns() {
		return m_graphProvider.getVertexNamespace();
	}
	
}
