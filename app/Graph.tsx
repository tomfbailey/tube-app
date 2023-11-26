'use client'
// Graph.tsx

import Cytoscape from 'cytoscape';
import React, { useEffect } from 'react';
import CytoscapeComponent from 'react-cytoscapejs';
import { ElementDefinition } from 'cytoscape';

import graphData from '../data/victoria.json';

    const Graph = () => {
        const cyRef = React.useRef<cytoscape.Core | undefined>();
        // useEffect(() => {
            

        // }, []); // Empty dependency array to run only on mount

        // Load in the json data
        const elements = CytoscapeComponent.normalizeElements(graphData);

        const stylesheet = [
            {
                selector: 'node[line = "victoria"]', // Select nodes with line=victoria
                style: {
                    'background-color': '#0098D4', // Set the background color to blue
                    'label': 'data(label)', // Display the node label
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'color': 'black',
                    'text-outline-color': '#0098D4',
                    'text-outline-width': '2px',
                    'text-outline-opacity': '1'
                }
            },
            {
                selector: 'edge[line = "victoria"]', // Select nodes with line=victoria
                style: {
                    'line-color': '#0098D4', // Set the background color to blue
                }
            }
        ];
    
        return (
            <CytoscapeComponent
                elements={elements}
                style={{ width: '1200px', height: '600px' }}
                stylesheet={stylesheet} // Apply the defined styles
                cy={(cy) => (cyRef.current = cy)}
            />
        );
    };

export default Graph;