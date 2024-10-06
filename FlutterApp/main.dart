import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'model/vacancy.dart';
//import 'vacancy_details.dart';  // Import the new details screen

class VacancyList extends StatefulWidget {
  VacancyList({super.key});

  @override
  State<VacancyList> createState() => _VacancyListState();
}

class _VacancyListState extends State<VacancyList> {
  List<Exercise> vacancies = [];

  Future<List<Exercise>> getData() async {
    try {
      var response = await http.get(Uri.parse('https://api.allorigins.win/get?url=https://unhcrjo.org/jobs/api'));

// After getting the response, extract the data:
      if (response.statusCode == 200) {
        var jsonData = jsonDecode(jsonDecode(response.body)['contents']);  // Get 'contents' from allorigins

        vacancies.clear(); // Clear previous data

        for (var eachVacancy in jsonData) {
          final vacancy = Exercise(
          squat: eachVacancy["squat"],
          biceps_right: eachVacancy["biceps_right"],
          biceps_left: eachVacancy["biceps_left"],
          triceps_right: eachVacancy["triceps_right"],
          triceps_left: eachVacancy["triceps_left"],
          back: eachVacancy["back"],
          );
          vacancies.add(vacancy);
        }

        return vacancies;
      } else {
        // Handle non-200 responses
        throw Exception('Failed to load vacancies: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to connect to the server. Please check your internet connection and try again.');
    }
  }

  @override
  Widget build(BuildContext context) {
    var screenWidth = MediaQuery.of(context).size.width;
    var screenHeight = MediaQuery.of(context).size.height;
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color(0xfffd980c),
        title: Text(
          'FitMinds',
          style: TextStyle(color: Color(0xff063568),fontWeight: FontWeight.bold,fontSize: 30),
        ),
      ),
      body: Padding(
        padding: EdgeInsets.all(screenHeight * 0.02),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            // Left Column
            Column(
              children: [
                Padding(
                  padding: const EdgeInsets.only(left: 50, top: 10),
                  child: Container(
                    height: screenHeight * 0.7, // 80% of column height
                    width: screenHeight * 0.7 * 1.2, // Maintain 1.2:1 ratio
                    decoration: BoxDecoration(
                      color: Colors.grey[200], // Border color
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(8.0), // Padding around the image
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(8), // Smaller corner radius for the inner image
                          image: DecorationImage(
                            image: AssetImage('assets/blank.png'), // Your image asset
                            fit: BoxFit.cover,
                          ),
                        ),
                      ),
                    ),
                  ),
                ),

                SizedBox(height: screenHeight * 0.02), // Spacer
                SizedBox(
                  height: screenHeight * 0.1, // 20% of column height
                  child: ElevatedButton(
                    onPressed: () {
                      // Add functionality for reset
                    },
                    child: Text('Reset',style: TextStyle(fontSize: 18),),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.grey[200], // Set the button color to gray
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8), // Less rounded corners
                      ),
                      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10), // Add padding
                      textStyle: TextStyle(fontSize: 16), // Adjust text size
                    ),
                  ),
                ),

              ],
            ),
            // Right Column
            Padding(
              padding: const EdgeInsets.only(right: 50),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  // First card: LeaderBoard
                  Card(
                    elevation: 4,
                    child: Container(
                      width: screenWidth * 0.4, // 40% of screen width
                      height: screenHeight * 0.25, // Adjust height of the card
                      child: Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'LeaderBoard',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8),
                            Text('Astronaut: SMM KG',style: TextStyle(fontSize: 13),),
                            SizedBox(height: 8),
                            //Text('Yousef: 31',style: TextStyle(fontSize: 16),),
                            Text('Anas: 28',style: TextStyle(fontSize: 16),),
                            Text('Sana: 22',style: TextStyle(fontSize: 16),),
                            Text('Doleh: 12',style: TextStyle(fontSize: 16),),
                          ],
                        ),
                      ),
                    ),
                  ),

                  // Second card: InBody
                  Card(
                    elevation: 4,
                    child: Container(
                      width: screenWidth * 0.4,
                      height: screenHeight * 0.15,
                      child: Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'InBody',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8),
                            Text('Weight: 82 kg',style: TextStyle(fontSize: 17),),
                            Text('Muscle Mass: 28 kg',style: TextStyle(fontSize: 17),),
                          ],
                        ),
                      ),
                    ),
                  ),

                  // Third card: ToDo
                  Card(
                    elevation: 4,
                    child: Container(
                      width: screenWidth * 0.4,
                      height: screenHeight * 0.3, // Adjust height for the checklist
                      child: Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'ToDo',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            //SizedBox(height: 8),
                            CheckboxListTile(
                              title: Text('Triceps',style: TextStyle(fontSize: 16),),
                              dense: true, // Makes the checkbox compact
                              contentPadding: EdgeInsets.all(0), // Further reduces space
                              value: false, // Change this based on your logic
                              onChanged: (newValue) {
                                // Handle the change
                              },
                            ),
                            CheckboxListTile(
                              title: Text('Biceps',style: TextStyle(fontSize: 16),),
                              dense: true,
                              contentPadding: EdgeInsets.all(0),
                              value: false,
                              onChanged: (newValue) {
                                // Handle the change
                              },
                            ),
                            CheckboxListTile(
                              title: Text('Back',style: TextStyle(fontSize: 16),),
                              dense: true,
                              contentPadding: EdgeInsets.all(0),
                              value: false,
                              onChanged: (newValue) {
                                // Handle the change
                              },
                            ),
                            CheckboxListTile(
                              title: Text('Squats',style: TextStyle(fontSize: 16),),
                              dense: true,
                              contentPadding: EdgeInsets.all(0),
                              value: false,
                              onChanged: (newValue) {
                                // Handle the change
                              },
                            ),
                          ],

                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),

          ],
        ),
      ),
    );
  }
}
