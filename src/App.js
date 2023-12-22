import React, { useState, useEffect } from 'react';
import './index.css';
import Confetti from 'react-confetti';
import nbaBackground from './nba_background.jpg';
import AtlantaHawks from './logos/AtlantaHawks.png';
import BostonCeltics from './logos/BostonCeltics.png';
import BrooklynNets from './logos/BrooklynNets.png';
import CharlotteHornets from './logos/CharlotteHornets.png';
import ChicagoBulls from './logos/ChicagoBulls.png';
import ClevelandCavaliers from './logos/ClevelandCavaliers.png';
import DallasMavericks from './logos/DallasMavericks.png';
import DenverNuggets from './logos/DenverNuggets.png';
import DetroitPistons from './logos/DetroitPistons.png';
import GoldenStateWarriors from './logos/GoldenStateWarriors.png';
import HoustonRockets from './logos/HoustonRockets.png';
import IndianaPacers from './logos/IndianaPacers.png';
import LosAngelesClippers from './logos/LosAngelesClippers.png';
import LosAngelesLakers from './logos/LosAngelesLakers.png';
import MemphisGrizzlies from './logos/MemphisGrizzlies.png';
import MiamiHeat from './logos/MiamiHeat.png';
import MilwaukeeBucks from './logos/MIlwaukeeBucks.png';
import MinnesotaTimberwolves from './logos/MinnesotaTimberwolves.png';
import NewOrleansPelicans from './logos/NewOrleansPelicans.png';
import NewYorkKnicks from './logos/NewYorkKnicks.png';
import OklahomaCityThunder from './logos/OklahomaCityThunder.png';
import OrlandoMagic from './logos/OrlandoMagic.png';
import Philadelphia76ers from './logos/Philadelphia76ers.png';
import PhoenixSuns from './logos/PhoenixSuns.png';
import PortlandTrailBlazers from './logos/PortlandTrailBlazers.png';
import SacramentoKings from './logos/SacramentoKings.png';
import SanAntonioSpurs from './logos/SanAntonioSpurs.png';
import TorontoRaptors from './logos/TorontoRaptors.png';
import UtahJazz from './logos/UtahJazz.png';
import WashingtonWizards from './logos/WashingtonWizards.png';

const nbaTeams = [
  'Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls',
  'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors',
  'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
  'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks',
  'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers',
  'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'
];

const teamLogos = {
  'Atlanta Hawks': AtlantaHawks,
  'Boston Celtics': BostonCeltics,
  'Brooklyn Nets': BrooklynNets,
  'Charlotte Hornets': CharlotteHornets,
  'Chicago Bulls': ChicagoBulls,
  'Cleveland Cavaliers': ClevelandCavaliers,
  'Dallas Mavericks': DallasMavericks,
  'Denver Nuggets': DenverNuggets,
  'Detroit Pistons': DetroitPistons,
  'Golden State Warriors': GoldenStateWarriors,
  'Houston Rockets': HoustonRockets,
  'Indiana Pacers': IndianaPacers,
  'Los Angeles Clippers': LosAngelesClippers,
  'Los Angeles Lakers': LosAngelesLakers,
  'Memphis Grizzlies': MemphisGrizzlies,
  'Miami Heat': MiamiHeat,
  'Milwaukee Bucks': MilwaukeeBucks,
  'Minnesota Timberwolves': MinnesotaTimberwolves,
  'New Orleans Pelicans': NewOrleansPelicans,
  'New York Knicks': NewYorkKnicks,
  'Oklahoma City Thunder': OklahomaCityThunder,
  'Orlando Magic': OrlandoMagic,
  'Philadelphia 76ers': Philadelphia76ers,
  'Phoenix Suns': PhoenixSuns,
  'Portland Trail Blazers': PortlandTrailBlazers,
  'Sacramento Kings': SacramentoKings,
  'San Antonio Spurs': SanAntonioSpurs,
  'Toronto Raptors': TorontoRaptors,
  'Utah Jazz': UtahJazz,
  'Washington Wizards': WashingtonWizards
};

function App() {
  const [team1, setTeam1] = useState('');
  const [team2, setTeam2] = useState('');
  const [team1Logo, setTeam1Logo] = useState(null);
  const [team2Logo, setTeam2Logo] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [predictionDisabled, setPredictionDisabled] = useState(false);

  const handleInputChange = (e, teamSetter, logoSetter) => {
    const { value } = e.target;
    teamSetter(value);
    logoSetter(teamLogos[value]);
  };

  useEffect(() => {
    setShowConfetti(false);
  }, [team1, team2]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setPredictionDisabled(true);

    if (team1 && team2) {
      fetch(`http://127.0.0.1:5000/predict?team1=${team1}&team2=${team2}`)
        .then(res => res.json())
        .then(prediction => {
          setData(prediction);
          setShowConfetti(true);
          setLoading(false);
          setPredictionDisabled(false);
          console.log(prediction);
        })
        .catch(error => {
          setLoading(false);
          setShowConfetti(false);
          setPredictionDisabled(false);
          console.error('Error fetching data:', error);
        });
    }
  };

  const handleReset = () => {
    setTeam1('');
    setTeam2('');
    setTeam1Logo(null);
    setTeam2Logo(null);
    setData(null);
    setShowConfetti(false);
    setLoading(false);
    setPredictionDisabled(false);
  };

  return (
    <div 
      className="bg-gradient-to-b from-gray-900 to-gray-700 text-white min-h-screen flex items-center justify-center"
      style={{ backgroundImage: `url(${nbaBackground})`, backgroundSize: 'cover', backgroundPosition: 'center' }}
    >
      <div className="bg-gray-800 bg-opacity-0 p-8 rounded-md shadow-md w-full max-w-md">
        <h1 className="text-3xl font-bold mb-8 text-center">
          Twitter API-Powered NBA Game Predictor
        </h1>

        <form onSubmit={handleSubmit}>
          <div className="mb-4 flex justify-center items-center">
            <div className="mr-4">
              <label htmlFor="team1" className="block text-sm font-medium">
                Team 1:
              </label>
              <select
                id="team1"
                name="team1"
                value={team1}
                onChange={(e) => handleInputChange(e, setTeam1, setTeam1Logo)}
                className="mt-1 p-2 border rounded-md w-full bg-gray-700 text-white"
                disabled={loading}
              >
                <option value="" disabled>Select Team 1</option>
                {nbaTeams.map((team, index) => (
                  <option key={index} value={team}>{team}</option>
                ))}
              </select>
              {team1Logo && (
                <img
                  src={team1Logo}
                  alt={`${team1} Logo`}
                  className="mt-2 max-w-full h-auto float-right"
                  style={{ maxHeight: '50px' }}
                />
              )}
            </div>
            <div>
              <label htmlFor="team2" className="block text-sm font-medium">
                Team 2:
              </label>
              <select 
                id="team2"
                name="team2"
                value={team2}
                onChange={(e) => handleInputChange(e, setTeam2, setTeam2Logo)}
                className="mt-1 p-2 border rounded-md w-full bg-gray-700 text-white"
                disabled={loading}
              >
                <option value="" disabled>Select Team 2</option>
                {nbaTeams.map((team, index) => (
                  <option key={index} value={team}>{team}</option>
                ))}
              </select>
              {team2Logo && (
                <img
                  src={team2Logo}
                  alt={`${team2} Logo`}
                  className="mt-2 max-w-full h-auto float-left"
                  style={{ maxHeight: '50px' }}
                />
              )}
            </div>
          </div>
          <div className="flex space-x-4">
            <button
              type="submit"
              className={`bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 ${loading || predictionDisabled ? 'opacity-50 cursor-not-allowed' : ''}`}
              disabled={loading || predictionDisabled}
            >
              {loading ? 'Predicting...' : 'Predict'}
            </button>
            <button
              type="button"
              onClick={handleReset}
              className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700"
            >
              Reset
            </button>
          </div>
        </form>

        {data && (
          <div className="mt-4 flex flex-col items-center">
            <p className="text-green-400 font-semibold">Prediction: {data} will win!</p>
            <img
              src={teamLogos[data]}
              alt={`${teamLogos[data]} Logo`}
              className="mt-2 max-w-full h-auto"
              style={{ maxHeight: '100px' }}
            />
            {showConfetti && (
              <Confetti
                width={window.innerWidth}
                height={window.innerHeight}
                numberOfPieces={2000}
                recycle={false}
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;