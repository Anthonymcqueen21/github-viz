package edu.brown.cs.fetch.frontend;

import java.util.Map;

import com.google.common.collect.ImmutableMap;
import com.google.gson.Gson;

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

		Map<String, Object> data = ImmutableMap.<String, Object> builder()
				.put("project_idea", project).build();

		Gson GSON = new Gson();
		return GSON.toJson(data);
	}

}
