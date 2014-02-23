package org.vpsc.entity;

import java.util.HashSet;
import java.util.Set;

public class Group {
	private int groupNumber;
	private String groupName;
	private Set<Category> category=new HashSet<Category>();
	public int getGroupNumber() {
		return groupNumber;
	}
	public void setGroupNumber(int groupNumber) {
		this.groupNumber = groupNumber;
	}
	public String getGroupName() {
		return groupName;
	}
	public void setGroupName(String groupName) {
		this.groupName = groupName;
	}
	public Set<Category> getCategory() {
		return category;
	}
	public void setCategory(Set<Category> category) {
		this.category = category;
	}

}
