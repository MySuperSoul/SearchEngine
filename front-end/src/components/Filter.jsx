import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import { DateRange } from '@material-ui/icons';
import Select from '@material-ui/core/Select';
// import Checkbox from '@material-ui/core/Checkbox';
// import Typography from '@material-ui/core/Typography';

const style = {
  formControl: {
    minWidth: 200,
    width: '40%',
    margin: '15px 0',
    // flexDirection: 'row',
    // alignItems: 'center'
  },
  sider: {
    display: 'flex',
    flexDirection: 'column'
  },
  label: {
    margin: '10px 0'
  }
}

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const options = {
  time: ['时间不限', '过去24小时内', '过去一周内', '过去一月内','过去一年内'],
  sources: ['CSDN', '简书', 'Coursera']
}

class Filter extends Component {
  state = {
    selectedTime: '时间不限',
    // selectedSources: []
  }

  handleTimeChange = (e) => {
    const index = options.time.indexOf(e.target.value)
    this.setState({
      selectedTime: e.target.value
    })
    this.props.changeTime(index);
  }

  handleSourceChange = value => () => {
    let items = this.state.selectedSources;
    let item = value;
    let newItems = [...items];
    let currentIndex = items.indexOf(item);
    if(currentIndex === -1) {
      newItems.push(item);
    } else {
      newItems.splice(currentIndex, 1);
    }
    console.log(newItems);

    this.setState({
      selectedSources: newItems
    })
  }

  render() {
    const { classes } = this.props;
    const { selectedTime } = this.state;
    return (
      <div className={classes.sider}>
        {/* <Typography variant="subtitle1" component="h2" className={classes.title}>
          条件筛选
        </Typography> */}
        <FormControl className={classes.formControl}>
          <FormLabel component="legend" className={classes.label}> 
            <DateRange /> 发布时间
          </FormLabel>
          <Select
            value={selectedTime}
            onChange={this.handleTimeChange}
            input={<Input id="select-multiple" />}
            MenuProps={MenuProps}
          >
            {options.time.map(time => (
              <MenuItem key={time} value={time}>
                {time}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </div>
    )
  }
}

export default withStyles(style)(Filter);