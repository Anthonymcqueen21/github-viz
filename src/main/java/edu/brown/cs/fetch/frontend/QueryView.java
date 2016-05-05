package edu.brown.cs.fetch.frontend;

import java.util.Map;

import com.google.common.collect.ImmutableMap;

import spark.ModelAndView;
import spark.Request;
import spark.Response;
import spark.TemplateViewRoute;

public class QueryView implements TemplateViewRoute {
	private String htmlUrl;

	QueryView(String htmlUrl) {
		this.htmlUrl = htmlUrl;
	}

	@Override
	public ModelAndView handle(Request request, Response response) {

		String idea = request.queryParams("idea");
		
		for (int i = 0; i < 1000000; i++) {
			System.out.println("yo");
		}
		
		
		
		
		Map<String, Object> variables = ImmutableMap.of("title",
				"Analysis", "idea", idea);
		return new ModelAndView(variables, htmlUrl);
	}

}
