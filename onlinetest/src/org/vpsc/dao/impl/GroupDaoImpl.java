package org.vpsc.dao.impl;

import java.io.Serializable;

import org.springframework.dao.DataAccessException;
import org.vpsc.dao.GroupDao;
import org.vpsc.entity.Group;

public class GroupDaoImpl extends CustomHibernateTemplate implements GroupDao {

	public int insertGroup(Group group) {
		// TODO Auto-generated method stub
		try{
			Serializable s=hTemplate.save(group);
			hTemplate.flush();
			return (Integer)s;
			}
			catch(DataAccessException dae){
				dae.printStackTrace();
				
				return -1;
			}
			
	}

}
