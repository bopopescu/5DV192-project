import React, { Component } from 'react'
import { Wrapper } from '../wrapper'

class ErrorNotFound extends Component {

    render() {
        return (
            <Wrapper>
                <div className="wrapper-error">
                    <div className="error-code">
                        404
                    </div>
                    <div className="error-message">
                        This page could not be found
                    </div>
                </div>
            </Wrapper>
        )
    }

}

export default ErrorNotFound
