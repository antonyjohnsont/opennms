package org.opennms.features.topology.plugins.topo.vmware.internal.operations;

import java.util.List;

import org.opennms.features.topology.api.Operation;
import org.opennms.features.topology.api.OperationContext;
import org.opennms.features.topology.plugins.topo.vmware.internal.VmwareTopologyProvider;


public class VmwareGenerateOperation implements Operation {

    VmwareTopologyProvider m_topologyProvider;

    public VmwareGenerateOperation(VmwareTopologyProvider topologyProvider) {
        m_topologyProvider = topologyProvider;
    }

    @Override
    public Undoer execute(List<Object> targets,
                          OperationContext operationContext) {

        m_topologyProvider.generate();

        return null;
    }

    @Override
    public boolean display(List<Object> targets, OperationContext operationContext) {
        return true;
    }

    @Override
    public boolean enabled(List<Object> targets, OperationContext operationContext) {
        return !m_topologyProvider.isGenerated();
    }

    @Override
    public String getId() {
        return null;
    }
}