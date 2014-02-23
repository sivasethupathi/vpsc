package org.vpsc.dao.impl;

import java.io.Serializable;

import org.springframework.dao.DataAccessException;
import org.vpsc.dao.TestDetailsDao;
import org.vpsc.entity.TestDetails;

public class TestDetailsDaoImpl extends CustomHibernateTemplate implements
		TestDetailsDao {

	public boolean testDetailsInsert(TestDetails testDetails) {
		try{
			Serializable s=hTemplate.save(testDetails);
			System.out.println(s);
			}
			catch(DataAccessException dae){
				return false;
			}
			return true;
	}

}
