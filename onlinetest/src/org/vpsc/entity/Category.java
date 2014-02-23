package org.vpsc.entity;

import java.util.HashSet;
import java.util.Set;

public class Category {
	private int categoryNumber;
	private String categoryName;
	private Group group;
	private Set<Question> questions=new HashSet<Question>();
	public int getCategoryNumber() {
		return categoryNumber;
	}
	public void setCategoryNumber(int categoryNumber) {
		this.categoryNumber = categoryNumber;
	}
	public String getCategoryName() {
		return categoryName;
	}
	public void setCategoryName(String categoryName) {
		this.categoryName = categoryName;
	}
	public Group getGroup() {
		return group;
	}
	public void setGroup(Group group) {
		this.group = group;
	}
	/* public boolean equals(Object obj) {
	      if (obj == null) return false;
	      if (!this.getClass().equals(obj.getClass())) return false;

	      Category obj2 = (Category)obj;
	      if((this.categoryNumber == obj2.getCategoryNumber()) && (this.categoryName.equals(obj2.getCategoryName())))
	      {
	         return true;
	      }
	      return false;
	   }
	   public int hashCode() {
	      int tmp = 0;
	      tmp = ( categoryNumber + categoryName ).hashCode();
	      return tmp;
	   }*/
	public Set<Question> getQuestions() {
		return questions;
	}
	public void setQuestions(Set<Question> questions) {
		this.questions = questions;
	}
}
