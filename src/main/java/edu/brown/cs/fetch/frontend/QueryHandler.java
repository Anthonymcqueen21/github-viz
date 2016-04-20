package edu.brown.cs.fetch.frontend;

import spark.QueryParamsMap;
import spark.Request;
import spark.Response;
import spark.Route;

class QueryHandler implements Route {

	@Override
	public Object handle(Request request, Response response) {
		QueryParamsMap qm = request.queryMap();
		String project = qm.value("project");
		System.out.println(project);
		return project;
	}

}
