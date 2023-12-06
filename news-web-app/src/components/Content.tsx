import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { getAnalytics, logEvent } from "firebase/analytics";

import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Tooltip from '@mui/material/Tooltip';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import RefreshIcon from '@mui/icons-material/Refresh';

import NewsTrendChart from "./NewsTrendChart";
import SentimentTrendChart from "./SentimentTrendChart";

export default function Content() {
  const analytics = getAnalytics();
  const navigate = useNavigate();
  const { pathname, search } = useLocation();

  const params = new URLSearchParams(search);
  const searchText = params.get("search") || ""; // 파라미터 가져오거나, 없으면 공백("")
  const [ inputText, setInputText ] = useState(searchText);

  function onSearch() {
    let url = pathname;

    if (inputText) {
      url += `?search=${inputText}`;
    }

    logEvent(analytics, "search", {inputText});

    navigate(url);
  }

  return (
    <Paper sx={{ maxWidth: 936, margin: 'auto', overflow: 'hidden' }}>
      <AppBar
        position="static"
        color="default"
        elevation={0}
        sx={{ borderBottom: '1px solid rgba(0, 0, 0, 0.12)' }}
      >
        <Toolbar>
          <Grid container spacing={2} alignItems="center">
            <Grid item>
              <SearchIcon color="inherit" sx={{ display: 'block' }} />
            </Grid>
            <Grid item xs>
              <TextField
                fullWidth
                placeholder="Search by keywords"
                InputProps={{
                  disableUnderline: true,
                  sx: { fontSize: 'default' },
                }}
                variant="standard"
                onChange = {(e) => {
                  setInputText(e.target.value);
                }}
                onKeyDown = {(e) => {
                  if (e.key === "Enter") {
                    onSearch();
                  }
                }}
                value ={inputText}
              />
            </Grid>
            <Grid item>
              <Button variant="contained"
                      sx={{ mr: 1 }}
                      onClick={onSearch}
              >
                Search
              </Button>
              <Tooltip title="Reload">
                <IconButton>
                  <RefreshIcon color="inherit" sx={{ display: 'block' }} />
                </IconButton>
              </Tooltip>
            </Grid>
          </Grid>
        </Toolbar>
      </AppBar>
      {
        pathname === "/news-trends" ?
        <NewsTrendChart search={searchText} /> :  <SentimentTrendChart search={searchText} />
      }
    </Paper>
  );
}
