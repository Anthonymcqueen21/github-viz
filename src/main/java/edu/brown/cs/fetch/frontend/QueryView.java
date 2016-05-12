package edu.brown.cs.fetch.frontend;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

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
		
//		HashMap<Integer, String> yearsToCSV = new HashMap<Integer, String>();
		
		class Printout implements Runnable {
		     private volatile String value;
		     private volatile Integer minYear;

		     @Override
		     public void run() {
		        value = new String();
		        minYear = new Integer(0);
		     }

		     public String getValue() {
		         return value;
		     }
		     
		     public String setString(String str) {
		    	 value = str;
		    	 return value;
		     }
		     
		     public Integer getInteger() {
		    	 return minYear;
		     }
		     
		     public Integer setInteger(int newInteger) {
		    	 minYear = newInteger;
		    	 return minYear;
		     }
		 }
		
		
		Printout printout = new Printout();
		
		// Create two threads
		Thread thread1 = new Thread(printout) {
//			private String printouts;
			
		    public void run() {
		    	printout.setString(runPhase1(idea));

		    	Thread thread11 = new Thread() {
		    		public void run() {
				    	generatePopularityAndOutput();
		    		}
		    	};
		    	
		    	Thread thread12 = new Thread(printout) {
				    public void run() {
				    	printout.setInteger(generateLanguage());
				    }
				};
				
		    	Thread thread13 = new Thread(printout) {
				    public void run() {
				    	runPredictor();
				    }
				};
		    	
				// Start the threads.
				thread11.start();
				thread12.start();
				thread13.start();
		    	
				// Wait for the two threads to finish
				try {
					thread11.join();
					thread12.join();
					thread13.join();
				} catch (InterruptedException e) {
					e.printStackTrace();
					System.out.println("ERROR: Problem joining threads.");
				}
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
		
		int numRepo = 1000;
		try {
//			System.out.println(printout.getValue().replace("We get ", "").replace(" items.", ""));
//			numRepo = Integer.parseInt(printout.getValue().replace("We get ", "").replace(" items.", ""));
			
			String mydata = printout.getValue();
			Pattern pattern = Pattern.compile("get (.*?) items");
			Matcher matcher = pattern.matcher(mydata);
			if (matcher.find())
			{
			    System.out.println(matcher.group(1));
			    numRepo = Integer.parseInt(matcher.group(1));
			}
			
			
		} catch (NumberFormatException e) {
			numRepo = 1000;
		}
		
		Map<String, Object> variables = ImmutableMap.of("title",
				"Analysis", "idea", idea, "minYear", printout.getInteger(), 
				"numRepositories", numRepo);
		return new ModelAndView(variables, htmlUrl);
	}
	
	
	private static String runPhase1(String idea) {
		
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
		return sb.toString();
	}
	
	private static void generatePopularityAndOutput() {
		File file = new File(System.getProperty("user.dir")
				+ "/data_mining/scripts(webapp_version)");
		
		System.out.println("Now executing:");
		System.out.println("python github_classifier.py");
		
		Process p = null;
		try {
			p = Runtime.getRuntime().exec("python github_classifier.py", null, file);
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("ERROR: Problem executing the github_classifier.py file.");
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
	
	private static Integer generateLanguage() {
		
		Integer minYear = Integer.MAX_VALUE;
		File file = new File(System.getProperty("user.dir")
				+ "/data_mining/scripts(webapp_version)");
		
		System.out.println("Now executing:");
		System.out.println("python pie_count.py");
		
		Process p = null;
		try {
			p = Runtime.getRuntime().exec("python pie_count.py", null, file);
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("ERROR: Problem executing the github_classifier.py file.");
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
				
//				String csvFile = line.substring(0, line.indexOf(" "));
				int year = Integer.parseInt(line.substring(line.indexOf(" ")+1));
				if (minYear > year) {
					minYear = year;
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("ERROR: Problem reading from the BufferedReader.");
		}
		
		System.out.println(sb.toString());
		
		return minYear;
	}
	
	private static void runPredictor() {
		File file = new File(System.getProperty("user.dir")
				+ "/data_mining/scripts(webapp_version)");
		
		System.out.println("Now executing:");
		System.out.println("python github_predictor.py");
		
		Process p = null;
		try {
			p = Runtime.getRuntime().exec("python github_predictor.py", null, file);
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("ERROR: Problem executing the github_predictor.py file.");
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
