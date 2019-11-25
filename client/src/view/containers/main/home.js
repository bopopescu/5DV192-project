import { connect } from 'react-redux'
import Home from '../../components/main/home'

function mapStateToProps(state) {
    return state;
}

const mapDispatchToProps = {
};

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Home)
