import Image from 'next/image'
import Graph from './Graph'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24" >

      <div className="relative flex place-items-center before:absolute before:h-[300px] before:w-[480px] before:-translate-x-1/2 before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-[240px] after:translate-x-1/3 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 before:lg:h-[360px] z-[-1]">
        <h1>Tube stuff</h1>
      </div>

      <div style={{ border: '2px solid black' }}>
        <Graph />
      </div>
      <p>
        Duis justo sapien, auctor a ligula eget, iaculis pharetra nulla. In sed malesuada arcu. Quisque viverra tortor
        sed imperdiet euismod. Aliquam quis sem vitae metus consequat posuere id ornare elit. Donec porttitor nulla id
        euismod luctus. In euismod a quam a convallis. Vivamus sit amet vehicula sapien, nec vulputate ex. Fusce non
        enim a felis luctus mattis ac nec nulla.
      </p>
    </main>
  )
}
