package org.vpsc.controller;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.context.support.WebApplicationContextUtils;
import org.vpsc.dao.QuestionDao;
import org.vpsc.entity.Question;

import jxl.*;
import jxl.read.biff.BiffException;
import jxl.write.*;

/**
 * Servlet implementation class question_upload
 */
public class question_upload extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public question_upload() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doPost(request, response);
		// TODO Auto-generated method stub
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response)  {
		// TODO Auto-generated method stub
		
		double num2=0;
		String s1=null;
		int row=0,col=0,i=0,j=0;
		int maxquiz=0;
		Cell a1 = null;
		NumberCell nc=null;
		LabelCell lc =null;
		
		
		try
		{
		PrintWriter out=response.getWriter();
		
		Set<Question> questions=new HashSet<Question>();
		
		Workbook workbook = Workbook.getWorkbook(new File("D:\\ALLY\\testa_upload\\test_dummy.xls"));
		Sheet sheet = workbook.getSheet(0);
		
		out.println("number of rows "+sheet.getRows());
		
		
		 
		for(i=1;i<sheet.getRows();i++)
		{
			out.println("<br><font size=10 color=red>i is "+i+"</font><font size=7 color=blue><br>");
				
			//a1 = sheet.getCell(column,row);
					
					Question q=new Question();
					
					//setting question number
					a1 = sheet.getCell(0,i);
					if (a1.getType() == CellType.NUMBER) 
					{ 
					nc = (NumberCell) a1; 
					q.setQuestionNumber((int) nc.getValue());
					}
					else if(a1.getType() ==CellType.LABEL)
					{
						out.println("cant upload... error in (0,"+i+") th cell");
					}
					
					
					//setting question name
					a1 = sheet.getCell(1,i);
					lc = (LabelCell) a1; 
					q.setQuestionName(lc.getString());
					
					//setting option1
					a1 = sheet.getCell(2,i);
					
					if (a1.getType() == CellType.NUMBER) 
					{ 
						nc = (NumberCell) a1;
						q.setOption1(nc.toString());
					}
					else
					{
						lc = (LabelCell) a1; 
						q.setOption1(lc.getString());
					}
					
					//setting option2
					a1 = sheet.getCell(3,i);
					if (a1.getType() == CellType.NUMBER) 
					{ 
						nc = (NumberCell) a1;
						q.setOption2(nc.toString());
					}
					else
					{
					lc = (LabelCell) a1; 
					q.setOption2(lc.getString());
					}

					//setting option3
					a1 = sheet.getCell(4,i);
					
					if (a1.getType() == CellType.NUMBER) 
					{ 
						nc = (NumberCell) a1;
						q.setOption3(nc.toString());
					}
					else
					{
					lc = (LabelCell) a1; 
					q.setOption3(lc.getString());
					}

					//setting option4
					a1 = sheet.getCell(5,i);
					if (a1.getType() == CellType.NUMBER) 
					{ 
						nc = (NumberCell) a1;
						q.setOption4(nc.toString());
					}
					else
					{
					lc = (LabelCell) a1; 
					q.setOption4(lc.getString());
					}

					//setting correct option
					a1 = sheet.getCell(6,i);
					lc = (LabelCell) a1; 
					q.setAnswer(lc.getString());

					//setting description
					a1 = sheet.getCell(7,i);
					lc = (LabelCell) a1; 
					q.setDescription(lc.getString());

					//setting reason
					a1 = sheet.getCell(8,i);
					lc = (LabelCell) a1; 
					q.setReason(lc.getString());

					//setting reference
					a1 = sheet.getCell(9,i);
					lc = (LabelCell) a1; 
					q.setReference(lc.getString());
					
					questions.add(q);
					out.println("</font><br>___________________________________________________");

		}

		out.println("out of for loop");


		Iterator iter = questions.iterator();
		i=0;
		while (iter.hasNext()) 
		{
			
			out.println("control entering into the while loop<br>size of set is "+questions.size());
			
			Question q=(Question)iter.next();
			
			out.println("<br>control after question iter");
			
			WebApplicationContext context = WebApplicationContextUtils.getRequiredWebApplicationContext(getServletContext());
			QuestionDao u = context.getBean("questionDaoImpl",QuestionDao.class);

		//	u.insertQuestion(q);

			out.println("uploading "+u.insertQuestion(q)+"th question");
		}
		
		out.println("questions uploaded");

		
				
		}catch( Exception e)
		{
			System.out.println( e.getMessage() );
			e.printStackTrace();
		}
	}

}
