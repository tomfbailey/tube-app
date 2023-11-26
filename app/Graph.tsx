'use client'
// Graph.tsx

import Cytoscape from 'cytoscape';
import React, { useEffect } from 'react';
import CytoscapeComponent from 'react-cytoscapejs';
import { ElementDefinition } from 'cytoscape';

import graphData from '../data/graph_data.json';

const lineColors = {
    bakerloo: '#B36305',
    central: '#E32017',
    circle: '#FFD300',
    district: '#00782A',
    'hammersmith-city': '#F3A9BB',
    jubilee: '#A0A5A9',
    metropolitan: '#9B0056',
    northern: '#000000',
    piccadilly: '#003688',
    victoria: '#0098D4',
    'waterloo-city': '#95CDBA',
    dlr: '#00A4A7',
    'london-overground': '#EE7C0E',
    'elizabeth': '#6950a1'
    // Add more lines and their respective colors as needed
};

const generateStylesheet = (colorsMap) => {
    const styles = [];
    
    // Write a style for all nodes (making them smaller)
    styles.push({
        selector: 'node',
        style: {
            'width': '20px',
            'height': '20px',
            'label': 'data(label)',
            'color': 'black',
            'font-size': '30px',
            'min-zoomed-font-size': '15px',
            // Make the node a white circle with a black border
            'background-color': 'white',
            'border-width': '4px',
            'border-color': 'black',
        },
    });

    styles.push({
        selector: 'edge',
        style: {
            'width': '10px',
            'curve-style': 'bezier'
        }
    });

    for (const line in colorsMap) {
        styles.push({
            selector: `edge[line = "${line}"]`,
            style: {
                'line-color': colorsMap[line],
            },
        });
    }
    return styles;
};



const Graph = () => {
    const cyRef = React.useRef<cytoscape.Core | undefined>();
    // useEffect(() => {
        

    // }, []); // Empty dependency array to run only on mount

    // Load in the json data
    const elements = CytoscapeComponent.normalizeElements(graphData);

    const stylesheet = generateStylesheet(lineColors);

    return (
        <CytoscapeComponent
            elements={elements}
            style={{ width: '1600px', height: '750px' }}
            stylesheet={stylesheet} // Apply the defined styles
            cy={(cy) => (cyRef.current = cy)}
        />
    );
};

export default Graph;