package org.vpsc.dao.impl;

import java.io.Serializable;

import org.springframework.dao.DataAccessException;
import org.vpsc.dao.LoginDao;
import org.vpsc.entity.Login;

public class LoginDaoImpl extends CustomHibernateTemplate implements LoginDao {

	public boolean createLogin(Login login) {
		try{
			Serializable s=hTemplate.save(login);
			System.out.println(s);
			}
			catch(DataAccessException dae){
				return false;
			}
			return true;
	}

}
