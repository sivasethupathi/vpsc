package org.vpsc.dao.impl;

import java.io.Serializable;

import org.springframework.dao.DataAccessException;
import org.vpsc.dao.QuestionDao;
import org.vpsc.entity.Question;

public class QuestionDaoImpl extends CustomHibernateTemplate implements
		QuestionDao {

	public boolean insertQuestion(Question question) {
		// TODO Auto-generated method stub
		try{
			Serializable s=hTemplate.save(question);
			System.out.println(s);
			}
			catch(DataAccessException dae){
				return false;
			}
			return true;
	}

}
