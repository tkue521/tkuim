import React, { Component } from 'react';
import './App.css';

import Header from '../components/Header/Header'
import WebcamCapture from '../components/Webcam/Webcam'
import Students from '../components/Students/Students'


class App extends Component {
  state = {
    studentsArray: []
  }

  deleteStudentHandler = (studentIndex) => {
    // Arrays and objects are reference types.
    // So need to call the spread operator (could alternately use the slice method),
    // to get a copy of the persons array- rather than a pointer to the
    // original array. Always update state in an immutable way.
    const students = [...this.state.studentsArray];
    students.splice(studentIndex, 1);
    this.setState({students: students});
  }
  
  // Grovery data from backend. 
  // The Webcam component sends an Axios POST request to the backend which returns the detected students
  // This data is passed to the state via the below callback, which the Webcam component executes.
  updateStudentStateHandler = (dataFromChild) => {
    const students = [...this.state.studentsArray];
    const totalStudents = students.concat(dataFromChild);
    
    // This code can be cleaned up be good enough for now!
    // each foreach loop should be contained within a function that can be reused. 
    // let nameHolder = {};
    // totalStudents.forEach(function (d) {
    //     if (nameHolder.hasOwnProperty(d.Name)) {
    //       nameHolder[d.Name] = nameHolder[d.Name] + d.price
    //     } else {       
    //       nameHolder[d.Name] = d.price
    //     }
    // });
    
    let idHolder = {};
    totalStudents.forEach(function (d) {
      // if (idHolder.hasOwnProperty(d.Name)) {
      //   idHolder[d.Name] = idHolder[d.name] + d.Id
      // } else {       
        idHolder[d.Name] = d.Id
      // }
    });

    let finalStudents = [];
    
    for(let prop in idHolder) {
      console.log(idHolder)
      finalStudents.push({Name: prop, Id: idHolder[prop]});   
    }

    this.setState({studentsArray: finalStudents});
  }

  render() {

    return (
        <div className='App bx--grid'>
          <Header/>
          <div className='bx--row'>
            <div className='bx--col-xs-6'>
              <WebcamCapture 
              callbackFromParent={this.updateStudentStateHandler}/>
            </div>
            <div className='bx--col-xs-6'>
              <Students
                students={this.state.studentsArray} 
                click={this.deleteStudentHandler}/>
            </div>
          </div>
        </div>

    );
  }
}

export default App;
