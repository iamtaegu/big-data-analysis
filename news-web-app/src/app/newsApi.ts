import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

import * as t from "./types";

export const newsApi = createApi({
    reducerPath: "news-api",
    baseQuery: fetchBaseQuery({
        baseUrl:
            "https://7yqpg0pc1k.execute-api.ap-northeast-2.amazonaws.com/dev/",
    }),
    endpoints: (builder) => ({
        //query<response, request>
        getNewsTrends: builder.query<t.NewsTrends, t.SearchReqParams>({
            query: ({ search }) => `news_trends?search=${search}`,
        }),
        getSentimentTrends: builder.query<t.SentimentTrends, t.SearchReqParams>({
            query: ({ search }) => `sentiment_trends?search=${search}`,
        })
    }),
});

export const { useGetNewsTrendsQuery, useGetSentimentTrendsQuery } = newsApi;