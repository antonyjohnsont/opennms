package org.opennms.netmgt.rrd.cassandra;

import java.util.Collections;

import me.prettyprint.cassandra.serializers.DoubleSerializer;
import me.prettyprint.cassandra.serializers.LongSerializer;
import me.prettyprint.cassandra.serializers.StringSerializer;
import me.prettyprint.hector.api.beans.HColumn;
import me.prettyprint.hector.api.beans.HSuperColumn;
import me.prettyprint.hector.api.factory.HFactory;
import me.prettyprint.hector.api.mutation.Mutator;


class Datapoint {
	String m_metricName;
	String m_dsName;
	long m_timestamp;
	double m_value;
	
	Datapoint(String metricName, String dsName, long timestamp, double value) {
		m_metricName = metricName;
		m_dsName = dsName;
		m_timestamp = timestamp;
		m_value = value;
	}
	
	public String getName() {
		return m_metricName;
	}
	
	public String getDsName() {
		return m_dsName;
	}

	public long getTimestamp() {
		return m_timestamp;
	}

	public double getValue() {
		return m_value;
	}

	public void perist(Mutator<String> mutator, String columnFamily, int ttl) {
		HColumn<String, Double> c = HFactory.createColumn(getDsName(), getValue(), ttl, StringSerializer.get(), DoubleSerializer.get());
		HSuperColumn<Long, String, Double> superColumn = HFactory.createSuperColumn(Long.valueOf(getTimestamp()), Collections.singletonList(c), LongSerializer.get(), StringSerializer.get(), DoubleSerializer.get());
		mutator.addInsertion(getName(), columnFamily, superColumn);

	}
	
	public String toString() {
		StringBuilder buf = new StringBuilder();
		buf.append(m_metricName).append("(").append(m_dsName).append("):");
		buf.append(m_timestamp).append("=").append(m_value);
		return buf.toString();
	}
}
