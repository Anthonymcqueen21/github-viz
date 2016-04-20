package edu.brown.cs.fetch.frontend;

/**
 * Interface for creating instances of spark servers.
 */
public interface SparkServer {
  /**
   * Starts the underlying spark server.
   */
  void runSparkServer();
}
