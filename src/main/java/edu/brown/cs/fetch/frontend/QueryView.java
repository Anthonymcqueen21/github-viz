package edu.brown.cs.fetch.frontend;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
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
		
		// Create two threads
		Thread thread1 = new Thread() {
		    public void run() {
		    	runPhase1(idea);
		    }
		};

		Thread thread2 = new Thread() {
		    public void run() {
		    	runGoogleTrendsFetcher(idea);
		    }
		};

		// Start the threads.
		thread1.start();
		thread2.start();

		// Wait for the two threads to finish
		try {
			thread1.join();
			thread2.join();
		} catch (InterruptedException e) {
			e.printStackTrace();
			System.out.println("ERROR: Problem joining threads.");
		}
		
		

		
		Map<String, Object> variables = ImmutableMap.of("title",
				"Analysis", "idea", idea);
		return new ModelAndView(variables, htmlUrl);
	}
	
	
	private static void runPhase1(String idea) {
		
		File file = new File(System.getProperty("user.dir")
				+ "/data_mining/scripts(webapp_version)");
		
		System.out.println("Now executing:");
		System.out.println("python phase1.py " + idea);
		
		Process p = null;
		try {
			p = Runtime.getRuntime().exec("python phase1.py " + idea, null, file);
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("ERROR: Problem executing the phase1.py file.");
		}
		try {
			p.waitFor();
		} catch (InterruptedException e) {
			e.printStackTrace();
			System.out.println("ERROR: Problem waiting for another thread.");
		}
		
		BufferedReader reader = new BufferedReader(new InputStreamReader(
				p.getInputStream()));

		StringBuilder sb = new StringBuilder();
		String line = "";
		try {
			while ((line = reader.readLine()) != null) {
				sb.append(line + "\n");
			}
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("ERROR: Problem reading from the BufferedReader.");
		}
		
		System.out.println(sb.toString());
	}
	
	private static void runGoogleTrendsFetcher(String idea) {
		
		File file = new File(System.getProperty("user.dir")
				+ "/data_mining/scripts(webapp_version)");
		
		System.out.println("Now executing:");
		System.out.println("python google_trends_fetcher.py " + idea);
		
		Process p = null;
		try {
			p = Runtime.getRuntime().exec("python google_trends_fetcher.py " + idea, null, file);
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("ERROR: Problem executing the google_trends_fetcher.py file.");
		}
		try {
			p.waitFor();
		} catch (InterruptedException e) {
			e.printStackTrace();
			System.out.println("ERROR: Problem waiting for another thread.");
		}
		
		BufferedReader reader = new BufferedReader(new InputStreamReader(
				p.getInputStream()));

		StringBuilder sb = new StringBuilder();
		String line = "";
		try {
			while ((line = reader.readLine()) != null) {
				sb.append(line + "\n");
			}
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("ERROR: Problem reading from the BufferedReader.");
		}
		
		System.out.println(sb.toString());
		
	}

}
