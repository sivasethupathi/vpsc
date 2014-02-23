package org.vpsc.dao.impl;

import java.io.Serializable;

import org.springframework.dao.DataAccessException;
import org.vpsc.dao.CategoryDao;
import org.vpsc.entity.Category;

public class CategoryDaoImpl extends CustomHibernateTemplate implements
		CategoryDao {

	public int insertCategory(Category category) {
		// TODO Auto-generated method stub
		try{
			Serializable s=hTemplate.save(category);
			return (Integer)s;
		//	System.out.println(category.getCategoryNumber()+""+category.getCategoryName()+""+category.getGroup().getGroupName());
			}
			catch(DataAccessException dae){
			//	System.out.println(category.getCategoryNumber()+""+category.getCategoryName()+""+category.getGroup().getGroupNumber());
				dae.printStackTrace();
				return -1;
			}
			

	}


}
