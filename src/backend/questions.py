"""
Interview Questions Module
Contains various categories of interview questions for practice sessions.
"""

from typing import List


def get_system_design_questions() -> List[str]:
    """
    Return a list of system design interview questions.

    Returns:
        List[str]: List of system design questions
    """
    questions = [
        "Design a URL shortener like bit.ly or TinyURL",
        "Design a social media feed like Twitter or Facebook",
        "Design a chat system like WhatsApp or Slack",
        "Design a video streaming platform like YouTube or Netflix",
        "Design a ride-sharing service like Uber or Lyft",
        "Design a search engine like Google",
        "Design an online marketplace like Amazon or eBay",
        "Design a notification system for mobile apps",
        "Design a distributed cache system like Redis",
        "Design a file storage service like Dropbox or Google Drive",
        "Design a recommendation system for e-commerce",
        "Design a web crawler system",
        "Design a real-time gaming leaderboard",
        "Design a food delivery system like DoorDash or UberEats",
        "Design a parking lot system",
        "Design a hotel booking system like Booking.com",
        "Design a distributed job scheduler",
        "Design a content delivery network (CDN)",
        "Design a messaging queue system like Apache Kafka",
        "Design a location-based service like Foursquare"
    ]
    return questions