package org.vpsc.test;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.vpsc.dao.constant.UserDetailsConstant;
import org.vpsc.dao.impl.LoginDaoImpl;
import org.vpsc.dao.impl.UserDetailsDaoImpl;
import org.vpsc.entity.Login;
import org.vpsc.entity.UserDetails;

public class UserDetailsTest {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		ApplicationContext context=new ClassPathXmlApplicationContext("spring-beans.xml");
		ApplicationContext testContext=new ClassPathXmlApplicationContext("test-data.xml");
		UserDetails userDetails=testContext.getBean("user1",UserDetails.class);
		Login login=testContext.getBean("login",Login.class);
		UserDetailsDaoImpl userDetailsImpl=context.getBean("userDetailsImpl",UserDetailsDaoImpl.class);
		LoginDaoImpl loginDaoImpl = context.getBean("loginDaoImpl",LoginDaoImpl.class);
		System.out.println("create userdetails status "+userDetailsImpl.createUserDetails(userDetails));
		int userId = userDetailsImpl.createUserDetails(userDetails);
		if(userId!=UserDetailsConstant.USER_CREATION_FAILED){
			login.setUserID(userId);
		System.out.println(loginDaoImpl.createLogin(login));
		}
		else{
		System.out.println("User Details Not Successful");	
		}
	}

}
