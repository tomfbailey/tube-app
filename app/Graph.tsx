'use client'
// Graph.tsx

import Cytoscape from 'cytoscape';
import React, { useEffect } from 'react';
import CytoscapeComponent from 'react-cytoscapejs';

const Graph = () => {
    const cyRef = React.useRef<cytoscape.Core | undefined>();
    // useEffect(() => {
        

    // }, []); // Empty dependency array to run only on mount
    const elements = CytoscapeComponent.normalizeElements({
        nodes: [
          { data: { id: 'one', label: 'Node 1' }, position: { x: 200, y: 500 } },
          { data: { id: 'two', label: 'Node 2' }, position: { x: 500, y: 200 } }
        ],
        edges: [
          {
            data: { source: 'one', target: 'two', label: 'Edge from Node1 to Node2' }
          }
        ]
      });

    // const layout = { name: 'random' };
 
    return <CytoscapeComponent elements={elements} 
    style={ { width: '1200px', height: '600px' } }
    // layout={layout}
    cy={(cy) => (cyRef.current = cy)} />;
};

export default Graph;