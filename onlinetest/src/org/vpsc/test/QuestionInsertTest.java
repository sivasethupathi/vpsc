package org.vpsc.test;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.vpsc.dao.GroupDao;
import org.vpsc.dao.QuestionDao;
import org.vpsc.entity.Category;
import org.vpsc.entity.Group;
import org.vpsc.entity.Question;

public class QuestionInsertTest {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		ApplicationContext context=new ClassPathXmlApplicationContext("spring-beans.xml");
		ApplicationContext testContext=new ClassPathXmlApplicationContext("test-data.xml");
		Category cat1=testContext.getBean("cat1",Category.class);
		cat1.getGroup().setGroupNumber(1);
		
		Question question=testContext.getBean("q1",Question.class);
		question.setCategory(cat1);
		QuestionDao questionDao=context.getBean("questionDaoImpl",QuestionDao.class);
		questionDao.insertQuestion(question);

	}

}
