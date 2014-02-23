package org.vpsc.dao.impl;

import org.springframework.orm.hibernate3.HibernateTemplate;

public class CustomHibernateTemplate {
	protected HibernateTemplate hTemplate;
	/**
	 * @param hTemplate the hTemplate to set
	 */
	public void sethTemplate(HibernateTemplate hTemplate) {
		this.hTemplate = hTemplate;
	}
}
