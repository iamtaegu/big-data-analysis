import './App.css';

import {Navigate, Route, Routes, useLocation} from "react-router-dom";
import { useEffect } from "react";

import Paperbase from "./components/Paperbase";
import NotFound from "./components/NotFound";
import { getAnalytics, logEvent } from "firebase/analytics";

export const NEWS_TRENDS_PATH = "/news-trends";
export const SENTIMENT_TRENDS_PATH = "/sentiment-trends";

function App() {

    const analytics = getAnalytics();
    const { pathname, search } = useLocation();

    useEffect(() => {
        const params = new URLSearchParams(search);

        logEvent(analytics, pathname, params);
    }, [analytics, pathname, search]);

    return (
        <Routes>
            <Route path="/" element={
                <Navigate to={NEWS_TRENDS_PATH} />}
            />
            <Route path={NEWS_TRENDS_PATH} element={<Paperbase />} />
            <Route path={SENTIMENT_TRENDS_PATH} element={<Paperbase />} />
            <Route path="*" element={<NotFound />} />
        </Routes>

    );
}

export default App;
