import React, { Component } from "react";
import Graph from "./Graph";

interface IState {
  data: any;
  showGraph: boolean;
}

class App extends Component<{}, IState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      data: null,
      showGraph: false,
    };
  }

  getData() {}

  pollServer(e: any) {
    e.currentTarget.disabled = true;
    let x = 0;
    const interval = setInterval(() => {
      fetch("http://localhost:5000/?sensor_type=all")
        .then((response) => response.text())
        .then((data) => {
          this.setState({
            data: JSON.parse(data),
            showGraph: true,
          });
        })
        .catch((error) =>
          console.log(`** Something went wrong with connection **\n${error}`)
        );
      x++;
      if (x > 500) {
        clearInterval(interval);
      }
    }, 250);
  }

  render() {
    return (
      <>
        <div className="App-header">Databank Time Series Simulator</div>
        <div className="App-content">
          {!this.state.showGraph && (
            <>
              <button
                className="Stream-button"
                onClick={(e) => this.pollServer(e)}
              >
                Start Streaming Data
              </button>
              <div className="Maintainers-wrapper">
                <h4>Maintainers:</h4>
                <div>Seun</div>
                <div>Israel</div>
                <div>James</div>
                <div>Daniel</div>
                <div>Owusu</div>
              </div>
            </>
          )}
          <div className="Graph">
            {this.state.showGraph && this.state.data && (
              <Graph data={this.state.data} />
            )}
          </div>
        </div>
      </>
    );
  }
}

export default App;
