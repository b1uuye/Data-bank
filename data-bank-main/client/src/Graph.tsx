import React, { Component } from "react";

class Graph extends Component<{ data: any }, {}> {
  table: any;

  componentDidMount() {
    const [elem]: any = document.getElementsByTagName("perspective-viewer");

    const schema = {
      uid: "string",
      timestamp: "datetime",
      location: "string",
      sensor_type: "string",
      sensor_id: "string",
      value: "float",
      ratio: "float",
      lower_bound: "float",
      upper_bound: "float",
      trigger_alert: "string",
    };

    if (window.perspective) {
      window.perspective
        .worker()
        .table(schema, { index: "uid" })
        .then((table: any) => {
          this.table = table;
          elem.load(this.table);
          elem.restore({ settings: true });
          this.updateTable();
        });
    }
  }

  componentDidUpdate() {
    this.updateTable();
  }

  componentWillUnmount() {
    this.table.delete();
  }

  updateTable() {
    if (this.table) {
      this.table.update([
        {
          uid: this.props.data.uid,
          timestamp: new Date(this.props.data.timestamp),
          location: this.props.data.location,
          sensor_type: this.props.data.sensor_type,
          sensor_id: this.props.data.sensor_id,
          value: this.props.data.value,
          ratio: this.props.data.ratio,
          lower_bound: this.props.data.lower_bound,
          upper_bound: this.props.data.upper_bound,
          trigger_alert: this.props.data.trigger_alert,
        },
      ]);
    }
  }

  render() {
    return React.createElement("perspective-viewer");
  }
}

export default Graph;
