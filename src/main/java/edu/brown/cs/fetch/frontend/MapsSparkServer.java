package edu.brown.cs.fetch.frontend;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.Map;

import com.google.common.collect.ImmutableMap;

import freemarker.template.Configuration;
import spark.ExceptionHandler;
import spark.ModelAndView;
import spark.Request;
import spark.Response;
import spark.Spark;
import spark.TemplateViewRoute;
import spark.template.freemarker.FreeMarkerEngine;

public class MapsSparkServer implements SparkServer {

	@Override
	public void runSparkServer() {
		Spark.externalStaticFileLocation("src/main/resources/static");
		Spark.exception(Exception.class, new ExceptionPrinter());
		FreeMarkerEngine freeMarker = createEngine();

		Spark.get("/", new MainHandler("main.ftl"), freeMarker);
		Spark.post("/query", new QueryHandler());
		Spark.get("/analysis", new QueryView("analysis.ftl"), freeMarker);

	}

	/**
	 * Private class to handle the serving of the main ftl template.
	 */
	private class MainHandler implements TemplateViewRoute {

		private String htmlUrl;

		public MainHandler(String htmlUrl) {
			this.htmlUrl = htmlUrl;
		}

		/**
		 * The handle method.
		 * 
		 * @param req
		 *            The request object.
		 * @param res
		 *            The response object.
		 */
		@Override
		public ModelAndView handle(Request req, Response res) {
			Map<String, Object> titleMap = ImmutableMap.of("title",
					"CS1951a: Final Project");

			return new ModelAndView(titleMap, htmlUrl);
		}
	}

	private static FreeMarkerEngine createEngine() {
		Configuration config = new Configuration();
		File templates = new File(
				"src/main/resources/spark/template/freemarker");
		try {
			config.setDirectoryForTemplateLoading(templates);
		} catch (IOException ioe) {
			System.out.printf("ERROR: Unable use %s for template loading.\n",
					templates);
			System.exit(1);
		}
		return new FreeMarkerEngine(config);
	}

	/**
	 * Private static method to handle exceptions and forwarding that to the
	 * GUI.
	 */
	private static class ExceptionPrinter implements ExceptionHandler {
		/**
		 * The handle method.
		 * 
		 * @param e
		 *            The exception throw.
		 * @param req
		 *            The request object.
		 * @param res
		 *            The response object.
		 */
		@Override
		public void handle(Exception e, Request req, Response res) {
			res.status(500);
			StringWriter stacktrace = new StringWriter();
			try (PrintWriter pw = new PrintWriter(stacktrace)) {
				pw.println("<pre>");
				e.printStackTrace(pw);
				pw.println("</pre>");
			}
			res.body(stacktrace.toString());
		}
	}

}
