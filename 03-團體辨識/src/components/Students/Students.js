import React from 'react';

import './Students.css';

import Student from './Student/Student';
import { Button } from 'carbon-components-react';
import { Icon } from 'carbon-components-react';

const Students = (props) => {
    return (
        <div className='table-button-group'>
            <div className='groceries-table'>
                <table className='bx--data-table-v2'>
                    <thead>
                        <tr>
                            <th>
                                <span className='.bx--table-header-label'>
                                    <h2>姓名</h2>
                                </span>
                            </th>
                            <th>
                                <span className='.bx--table-header-label'>
                                    <h2>學號</h2>
                                </span>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {props.students.map(student => {
                            return <Student
                            // key={student.Key}
                            key={student.Name}
                            Name={student.Name}
                            Id={student.Id}/>
                        })}
                    </tbody>
                </table>
            </div>
            <div className='pay-now-button-container'>
                <Button
                    className='pay-now-button'>點名
                <Icon 
                    className='arrow-right'
                    name='icon--arrow--right'
                    fill='white'/>
                </Button>
            </div>
        </div>
        
    )
}

export default Students