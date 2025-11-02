"""
Ultra-Versatile Input Guardrail for JEE Math/Physics/Chemistry
Supports CBSE, ICSE, State Boards + JEE, NEET
"""

import re

class GuardrailService:
    """Only allows Math, Physics, Chemistry questions"""
    
    def __init__(self):
        # ALLOWED KEYWORDS - Comprehensive Math/Physics/Chemistry
        self.allowed_keywords = {
            # ============ BASIC ARITHMETIC ============
            'calculate', 'add', 'subtract', 'multiply', 'divide',
            'plus', 'minus', 'times', 'divided', 'equals',
            'result', 'answer', 'compute', 'what', 'how much',
            'sum', 'product', 'quotient', 'remainder', 'arithmetic',
            
            # ============ ALGEBRA ============
            'solve', 'equation', 'linear', 'quadratic', 'cubic',
            'polynomial', 'expand', 'factor', 'factorize',
            'simplify', 'expression', 'variable', 'coefficient',
            'inequality', 'absolute', 'value', 'root', 'radical',
            'exponent', 'power', 'logarithm', 'log', 'ln',
            'exponential', 'algebraic', 'term', 'degree',
            'rational', 'irrational', 'surds', 'indices',
            
            # ============ GEOMETRY ============
            'geometry', 'geometric', 'area', 'perimeter', 'volume',
            'surface', 'triangle', 'square', 'rectangle', 'circle',
            'polygon', 'cone', 'cylinder', 'sphere', 'prism',
            'angle', 'degrees', 'radian', 'right', 'obtuse', 'acute',
            'parallel', 'perpendicular', 'tangent', 'chord', 'diameter',
            'radius', 'circumference', 'arc', 'sector', 'segment',
            'altitude', 'median', 'bisector', 'centroid',
            'congruent', 'similar', 'symmetry', '3d', 'coordinate',
            
            # ============ TRIGONOMETRY ============
            'trigonometry', 'sin', 'cos', 'tan', 'sec', 'csc', 'cot',
            'sine', 'cosine', 'tangent', 'secant', 'cosecant', 'cotangent',
            'inverse', 'arcsin', 'arccos', 'arctan', 'asin', 'acos', 'atan',
            'trigonometric', 'identity', 'angle', 'radian', 'degree',
            'sine rule', 'cosine rule', 'pythagorean',
            
            # ============ CALCULUS ============
            'calculus', 'derivative', 'differentiate', 'integration', 'integrate',
            'integral', 'limit', 'continuous', 'differentiable',
            'function', 'curve', 'slope', 'tangent', 'normal',
            'maximum', 'minimum', 'optimization', 'rate', 'change',
            'chain rule', 'product rule', 'quotient rule',
            'partial', 'gradient', 'divergence', 'curl',
            'series', 'sequence', 'convergence', 'divergence',
            
            # ============ STATISTICS & PROBABILITY ============
            'statistics', 'probability', 'mean', 'median', 'mode',
            'standard', 'deviation', 'variance', 'distribution',
            'normal', 'binomial', 'poisson', 'permutation', 'combination',
            'ncr', 'npr', 'factorial', 'likelihood', 'expected', 'value',
            'histogram', 'scatter', 'correlation', 'regression',
            'sample', 'population', 'frequency', 'cumulative',
            
            # ============ MATRICES & VECTORS ============
            'matrix', 'matrices', 'vector', 'determinant', 'inverse',
            'eigenvalue', 'eigenvector', 'trace', 'rank',
            'dot product', 'cross product', 'scalar', 'magnitude',
            'linear algebra', 'transpose', 'orthogonal', 'diagonal',
            
            # ============ NUMBER THEORY ============
            'prime', 'composite', 'factor', 'divisor', 'multiple',
            'gcf', 'lcm', 'gcd', 'coprime', 'modulo', 'mod',
            'number theory', 'divisibility', 'digit', 'sum', 'perfect',
            'fibonacci', 'armstrong', 'palindrome',
            
            # ============ PROOF & LOGIC ============
            'prove', 'proof', 'theorem', 'lemma', 'corollary',
            'axiom', 'postulate', 'hypothesis', 'conclusion',
            'induction', 'contradiction', 'logical', 'truth',
            
            # ============ PHYSICS - MECHANICS ============
            'force', 'velocity', 'acceleration', 'speed', 'displacement',
            'distance', 'motion', 'mass', 'weight', 'gravity',
            'momentum', 'impulse', 'friction', 'tension',
            'pressure', 'density', 'buoyancy', 'drag',
            'newton', 'laws', 'mechanics', 'kinematics', 'dynamics',
            'circular', 'projectile', 'work', 'energy', 'power',
            'kinetic', 'potential', 'conservation', 'collision',
            'upward', 'downward', 'horizontal', 'vertical', 'throw', 'thrown',
            'ball', 'object', 'body', 'particle', 'block',
            
            # ============ PHYSICS - THERMODYNAMICS ============
            'heat', 'temperature', 'thermodynamics', 'entropy',
            'enthalpy', 'internal', 'energy', 'law',
            'isothermal', 'adiabatic', 'isobaric', 'isochoric',
            'expansion', 'compression', 'specific', 'capacity',
            'calorimeter', 'latent', 'fusion', 'vaporization',
            
            # ============ PHYSICS - WAVES & SOUND ============
            'wave', 'waves', 'frequency', 'wavelength', 'amplitude',
            'period', 'velocity', 'sound', 'echo', 'doppler',
            'interference', 'diffraction', 'superposition',
            'resonance', 'decibel', 'transverse', 'longitudinal',
            
            # ============ PHYSICS - OPTICS ============
            'optics', 'light', 'reflection', 'refraction', 'lens',
            'mirror', 'image', 'focal', 'distance', 'magnification',
            'dispersion', 'prism', 'spectrum', 'diffraction',
            'polarization', 'interference', 'critical', 'angle',
            'snell', 'law', 'refractive', 'index',
            
            # ============ PHYSICS - ELECTROMAGNETISM ============
            'electric', 'electricity', 'charge', 'current', 'voltage',
            'resistance', 'resistivity', 'capacitor', 'capacitance',
            'inductor', 'inductance', 'circuit', 'ohm', 'amp', 'volt',
            'magnetic', 'magnetism', 'field', 'flux', 'torque',
            'solenoid', 'transformer', 'motor', 'generator',
            'electromagnetic', 'induction', 'faraday', 'ampere',
            'coulomb', 'force', 'potential', 'energy', 'power', 'factor',
            
            # ============ PHYSICS - MODERN & QUANTUM ============
            'quantum', 'photon', 'electron', 'atomic', 'nuclear',
            'atom', 'nucleus', 'proton', 'neutron', 'radioactive',
            'decay', 'half-life', 'isotope', 'fission', 'fusion',
            'relativity', 'mass', 'energy', 'einstein',
            'planck', 'schrodinger', 'uncertainty', 'principle',
            
            # ============ CHEMISTRY - PHYSICAL ============
            'chemistry', 'chemical', 'reaction', 'element', 'compound',
            'atom', 'molecule', 'mole', 'molarity', 'molality',
            'concentration', 'solution', 'solubility', 'titration',
            'acid', 'base', 'ph', 'poh', 'buffer', 'salt', 'ester',
            'equilibrium', 'rate', 'kinetics', 'catalyst', 'activation',
            'enthalpy', 'entropy', 'gibbs', 'thermodynamic',
            
            # ============ CHEMISTRY - ORGANIC ============
            'organic', 'carbon', 'hydrocarbon',
            'alkane', 'alkene', 'alkyne', 'aromatic', 'benzene',
            'functional', 'group', 'alcohol', 'aldehyde', 'ketone',
            'carboxylic', 'ester', 'ether', 'amine', 'amide',
            'isomer', 'isomerism', 'stereoisomer', 'enantiomer',
            'substitution', 'addition', 'elimination',
            'mechanism', 'nucleophile', 'electrophile', 'radical',
            
            # ============ CHEMISTRY - INORGANIC ============
            'inorganic', 'metal', 'nonmetal', 'metalloid', 'noble',
            'valency', 'oxidation', 'reduction', 'redox', 'bond',
            'ionic', 'covalent', 'metallic', 'hydrogen', 'coordinate',
            'lewis', 'structure', 'vsepr', 'hybridization',
            'coordination', 'complex', 'ligand', 'transition',
            
            # ============ CHEMISTRY - PERIODIC TABLE ============
            'periodic', 'table', 'group', 'period', 'block',
            's-block', 'p-block', 'd-block', 'f-block',
            'alkali', 'alkaline', 'earth', 'halogen', 'chalcogen',
            'lanthanide', 'actinide', 'trend', 'electronegativity',
            
            # ============ QUERIES & OPERATIONS ============
            'find', 'calculate', 'evaluate', 'determine', 'show',
            'prove', 'verify', 'check', 'balance', 'draw', 'sketch',
            'plot', 'graph', 'table', 'list', 'explain', 'describe',
            '=', '+', '-', '*', '/', '^', '√', 'π', '∫', '∑',
        }
        
        # STRICTLY BLOCKED - Use WORD BOUNDARIES to avoid "upward"/"war" issue
        self.blocked_patterns = [
            # Daily life
            r'\brecipe\b', r'\bcook\b', r'\bfood\b', r'\bdish\b', r'\bmeal\b', 
            r'\bbiryani\b', r'\bbriyani\b', r'\bweather\b', r'\brain\b',
            
            # Entertainment
            r'\bjoke\b', r'\bfunny\b', r'\blaugh\b', r'\bhumor\b', r'\bmovie\b',
            r'\bfilm\b', r'\bmusic\b', r'\bsong\b', r'\bgame\b', r'\bplay\b',
            r'\bsport\b', r'\bcricket\b', r'\bfootball\b', r'\bactor\b',
            
            # Non-STEM subjects
            r'\bbiology\b', r'\bbotany\b', r'\bzoology\b', r'\banatomy\b',
            r'\bcell\b', r'\bdna\b', r'\bgene\b', r'\bhistory\b', r'\bgeography\b',
            r'\bpolitics\b', r'\beconomics\b', r'\bsociology\b', r'\bliterature\b',
            r'\benglish\b', r'\bgrammar\b', r'\bessay\b', r'\bpoem\b', r'\bnovel\b',
            
            # Tech (not academic science)
            r'\bprogramming\b', r'\bcode\b', r'\bpython\b', r'\bjava\b',
            r'\bjavascript\b', r'\bwebsite\b', r'\bapp\b', r'\bsoftware\b',
            
            # Harmful - WORD BOUNDARIES PREVENT "upward"/"war" FALSE MATCH
            r'\bweapon\b', r'\bgun\b', r'\bknife\b', r'\bbomb\b', r'\bexplosive\b',
            r'\battack\b', r'\bkill\b', r'\bmurder\b', r'\bharm\b', r'\bviolence\b',
            r'\bfight\b', r'\bwar\b',  # Now only matches " war ", not "upward"
            r'\bdrug\b', r'\bpoison\b', r'\billegal\b', r'\bcrime\b', r'\bsteal\b',
            r'\bhack\b',
            
            # Business
            r'\bbusiness\b', r'\bcompany\b', r'\bstock\b', r'\bmarket\b',
            r'\bprofit\b', r'\bsales\b', r'\bmarketing\b', r'\bstartup\b',
            
            # Personal
            r'\brelationship\b', r'\bdating\b', r'\blove\b', r'\bfriend\b',
            r'\bfamily\b', r'\bpersonal\b',
        ]
    
    def is_academic_question(self, question: str) -> tuple[bool, str]:
        """
        VERSATILE: Math/Physics/Chemistry for CBSE/ICSE/JEE/NEET
        Uses WORD BOUNDARIES to avoid false matches.
        
        Returns:
            (is_valid, reason)
        """
        question_lower = question.lower()
        
        # STEP 1: Block forbidden keywords with WORD BOUNDARIES
        for blocked_pattern in self.blocked_patterns:
            if re.search(blocked_pattern, question_lower):
                matched_word = blocked_pattern.replace(r'\b', '')
                return False, f"🚫 BLOCKED: '{matched_word}' detected. Only Math/Physics/Chemistry questions allowed."
        
        # STEP 2: MUST contain at least ONE allowed keyword
        has_academic = any(kw in question_lower for kw in self.allowed_keywords)
        if not has_academic:
            return False, "🚫 No Math/Physics/Chemistry keywords detected. Please ask an academic science question."
        
        # STEP 3: Length check
        if len(question.strip()) < 2:
            return False, "🚫 Question too short"
        
        # All checks passed
        return True, "✅ Valid academic question"


# Initialize service
guardrail = GuardrailService()
