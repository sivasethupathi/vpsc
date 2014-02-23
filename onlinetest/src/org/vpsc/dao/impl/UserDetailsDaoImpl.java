package org.vpsc.dao.impl;

import java.io.Serializable;

import org.springframework.dao.DataAccessException;
import org.vpsc.dao.UserDetailsDao;
import org.vpsc.dao.constant.UserDetailsConstant;
import org.vpsc.entity.UserDetails;

public class UserDetailsDaoImpl extends CustomHibernateTemplate implements UserDetailsDao {

	public int createUserDetails(UserDetails userDetails) {
		// TODO Auto-generated method stub
		int s;
		try{
		s=(Integer)hTemplate.save(userDetails);
		System.out.println(s);
		}
		catch(DataAccessException dae){
			return UserDetailsConstant.USER_CREATION_FAILED;
		}
		return s;
	}

}
