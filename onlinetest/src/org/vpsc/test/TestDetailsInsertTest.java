package org.vpsc.test;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.vpsc.dao.QuestionDao;
import org.vpsc.dao.TestDetailsDao;
import org.vpsc.entity.Category;
import org.vpsc.entity.Question;
import org.vpsc.entity.TestDetails;

public class TestDetailsInsertTest {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		ApplicationContext context=new ClassPathXmlApplicationContext("spring-beans.xml");
		ApplicationContext testContext=new ClassPathXmlApplicationContext("test-data.xml");
		Category cat1=testContext.getBean("cat1",Category.class);
		cat1.getGroup().setGroupNumber(1);
		
		TestDetails testDetails=testContext.getBean("t1",TestDetails.class);
		
		TestDetailsDao testDetailsDao=context.getBean("testDetailsDaoImpl",TestDetailsDao.class);
		testDetailsDao.testDetailsInsert(testDetails);
	}

}
