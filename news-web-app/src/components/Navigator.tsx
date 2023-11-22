import * as React from 'react';
import { useNavigate, useLocation } from "react-router-dom";

import Drawer, { DrawerProps } from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListItemButton from '@mui/material/ListItemButton';
import PeopleIcon from '@mui/icons-material/People';
import DnsRoundedIcon from '@mui/icons-material/DnsRounded';
import PermMediaOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActual';
import PublicIcon from '@mui/icons-material/Public';
import SettingsEthernetIcon from '@mui/icons-material/SettingsEthernet';
import SettingsInputComponentIcon from '@mui/icons-material/SettingsInputComponent';
import TimerIcon from '@mui/icons-material/Timer';
import SettingsIcon from '@mui/icons-material/Settings';
import PhonelinkSetupIcon from '@mui/icons-material/PhonelinkSetup';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ShowChartIcon from '@mui/icons-material/ShowChart';

import { NEWS_TRENDS_PATH, SENTIMENT_TRENDS_PATH } from '../App';

const categories = [
  {
    id: 'Build',
    children: [
      {
        id: 'Authentication',
        icon: <PeopleIcon />,
        active: true,
      },
      { id: 'Database', icon: <DnsRoundedIcon /> },
      { id: 'Storage', icon: <PermMediaOutlinedIcon /> },
      { id: 'Hosting', icon: <PublicIcon /> },
      { id: 'Functions', icon: <SettingsEthernetIcon /> },
      {
        id: 'Machine learning',
        icon: <SettingsInputComponentIcon />,
      },
    ],
  },
  {
    id: 'Quality',
    children: [
      { id: 'Analytics', icon: <SettingsIcon /> },
      { id: 'Performance', icon: <TimerIcon /> },
      { id: 'Test Lab', icon: <PhonelinkSetupIcon /> },
    ],
  },
];

const item = {
  py: '2px',
  px: 3,
  color: 'rgba(255, 255, 255, 0.7)',
  '&:hover, &:focus': {
    bgcolor: 'rgba(255, 255, 255, 0.08)',
  },
};

const itemCategory = {
  boxShadow: '0 -1px 0 rgb(255,255,255,0.1) inset',
  py: 1.5,
  px: 3,
};

export default function Navigator(props: DrawerProps) {
  const { ...other } = props;
  const navigate = useNavigate();
  const { pathname } = useLocation(); // 오른쪽 객체에서 pathname 만 사용하겠음

  // redundancy 제거 & 가독성 향상
  const menus = [
    {
      title: 'News Trends',
      path: NEWS_TRENDS_PATH,
      icon: <ShowChartIcon />,
    },
    {
      title: 'Sentiment Trends',
      path: SENTIMENT_TRENDS_PATH,
      icon: <FavoriteIcon />,
    },
  ]

  return (
    <Drawer variant="permanent" {...other}>
      <List disablePadding>
        <ListItem sx={{ ...item, ...itemCategory, fontSize: 22, color: '#fff' }}>
          News Analytics
        </ListItem>
        {
          menus.map(({title, path, icon}) => (
            <ListItem sx={{ ...item, ...itemCategory }}>
            <ListItemButton
                selected={pathname === path}
                onClick={() => {
                  navigate(path);
                }}
            >
              <ListItemIcon>
                {icon}
              </ListItemIcon>
              <ListItemText>{title}</ListItemText>
            </ListItemButton>
          </ListItem>))
        }
      </List>
    </Drawer>
  );
}
