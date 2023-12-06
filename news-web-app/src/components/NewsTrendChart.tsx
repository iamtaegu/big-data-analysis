import React from 'react';
import Plot from 'react-plotly.js';

import { useGetNewsTrendsQuery } from "../app/newsApi";

import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";

interface IProps {
    search: string;
}

export default function NewsTrendChart({ search }: IProps) {
    const { data, isLoading } = useGetNewsTrendsQuery({search: search});

    if (isLoading || !data) {
        return (
            <Box sx={{ p:3, textAlign: "center" }}>
                <CircularProgress />
            </Box>
        );
    }

    const trace: Plotly.Data = {
        x: data.message.map((el) => el.date),
        y: data.message.map((el) => el.doc_count),
        type: "scatter",
        mode: "lines+markers",
    }

    return (
        <Plot
            data={[trace]}
            layout={ {autosize: true} }
            style={ {width: "100%"} }
        />
    );
}