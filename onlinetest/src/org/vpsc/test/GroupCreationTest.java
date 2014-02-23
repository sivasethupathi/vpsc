package org.vpsc.test;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.vpsc.dao.CategoryDao;
import org.vpsc.dao.GroupDao;
import org.vpsc.entity.Category;
import org.vpsc.entity.Group;

public class GroupCreationTest {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		ApplicationContext context=new ClassPathXmlApplicationContext("spring-beans.xml");
		ApplicationContext testContext=new ClassPathXmlApplicationContext("test-data.xml");
		Group group=testContext.getBean("group",Group.class);
		GroupDao groupDao=context.getBean("groupDaoImpl",GroupDao.class);
		int gno=groupDao.insertGroup(group);
		System.out.println(gno+"\n\n");
		
		
		Category cat1=testContext.getBean("cat1",Category.class);
		Category cat2=testContext.getBean("cat2",Category.class);
		
		cat1.getGroup().setGroupNumber(gno);
		cat2.getGroup().setGroupNumber(gno);
		CategoryDao categoryDao=context.getBean("categoryDaoImpl",CategoryDao.class);
		System.out.println(categoryDao.insertCategory(cat1));
		System.out.println(categoryDao.insertCategory(cat2));
	}

}
