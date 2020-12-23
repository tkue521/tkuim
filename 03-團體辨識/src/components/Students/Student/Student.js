import React from 'react';

const Student = (props) => {
    return (
        <tr onClick={props.click}>
            <td><h3>{props.Name}</h3></td>
            <td><h3>{props.Id}</h3></td>
        </tr>
    )
}

export default Student