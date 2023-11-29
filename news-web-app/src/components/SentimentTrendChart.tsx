import React from 'react';
import Plot from 'react-plotly.js';

import { useGetSentimentTrendsQuery } from "../app/newsApi";

import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";

interface IProps {
    search: string;
}

export default function SentimentTrendChart({ search }: IProps) {
    const { data, isLoading } = useGetSentimentTrendsQuery({search: search});

    if (isLoading || !data) {
        return (
            <Box sx={{ p:3, textAlign: "center" }}>
                <CircularProgress />
            </Box>
        );
    }

    /* const trace1: Plotly.Data = {
        x: data.message.map((el: any) => el.date),
        y: data.message.map((el: any) => el.positive),
        type: "scatter",
        mode: "lines+markers",
        name: "Positive",
    }

    const trace2: Plotly.Data = {
        x: data.message.map((el: any) => el.date),
        y: data.message.map((el: any) => el.neutral),
        type: "scatter",
        mode: "lines+markers",
        name: "Neutral",
    }

    const trace3: Plotly.Data = {
        x: data.message.map((el: any) => el.date),
        y: data.message.map((el: any) => el.negative),
        type: "scatter",
        mode: "lines+markers",
        name: "Negative",
    } */

    const traces: Plotly.Data[] = [
        'positive', 'neutral', 'negative',
    ].map((x) => ({
        x: data.message.map((el: any) => el.date),
        y: data.message.map((el: any) => (el as any)[x]),
        type: "scatter",
        mode: "lines+markers",
        name: x,
    }))

    return (
        <Plot
            // data={[trace1, trace2, trace3]}
            data={traces}
            layout={ {autosize: true} }
            style={ {width: "100%"} }
        />
    );
}