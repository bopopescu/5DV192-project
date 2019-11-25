import Reactotron from 'reactotron-react-js'
import { reactotronRedux } from 'reactotron-redux'

const ENABLE_REACTOTRON = false;

Reactotron.configure().use(reactotronRedux());

if (ENABLE_REACTOTRON && (
        window.location.hostname === "localhost" ||
        window.location.hostname === "127.0.0.1"
)) {
    Reactotron.connect() // development server, connect reactotron
}

export default Reactotron
