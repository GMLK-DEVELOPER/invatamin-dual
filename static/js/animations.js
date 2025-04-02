// 3D Background Animation with Three.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize background animation
    initBackgroundAnimation();
    
    // Initialize counters for statistics
    initCounters();
    
    // Initialize testimonial slider
    initTestimonialSlider();
    
    // Initialize glitch effect
    initGlitchEffect();
    
    // Initialize accordions
    initAccordions();
    
    // Set data-text attribute for glitch effect
    const glitchTexts = document.querySelectorAll('.glitch-text');
    glitchTexts.forEach(text => {
        text.setAttribute('data-text', text.textContent);
    });
});

// Background Animation with THREE.js
function initBackgroundAnimation() {
    const canvas = document.getElementById('background-canvas');
    if (!canvas) return;
    
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    
    const renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    canvas.appendChild(renderer.domElement);
    
    // Create particles
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 2000;
    
    const posArray = new Float32Array(particlesCount * 3);
    const colors = new Float32Array(particlesCount * 3);
    
    for (let i = 0; i < particlesCount * 3; i += 3) {
        // Position
        posArray[i] = (Math.random() - 0.5) * 10;
        posArray[i + 1] = (Math.random() - 0.5) * 10;
        posArray[i + 2] = (Math.random() - 0.5) * 10;
        
        // Color - purple shades
        colors[i] = Math.random() * 0.5 + 0.5; // R
        colors[i + 1] = Math.random() * 0.3; // G
        colors[i + 2] = Math.random() * 0.5 + 0.5; // B
    }
    
    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    
    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.02,
        transparent: true,
        opacity: 0.8,
        vertexColors: true,
        blending: THREE.AdditiveBlending
    });
    
    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);
    
    camera.position.z = 5;
    
    // Add floating 3D cube if exists
    const floatingCube = document.getElementById('floating-cube');
    if (floatingCube) {
        const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
        const cubeMaterial = new THREE.MeshBasicMaterial({ 
            color: 0x8c00ff,
            wireframe: true
        });
        const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
        
        const cubeScene = new THREE.Scene();
        const cubeCamera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
        
        const cubeRenderer = new THREE.WebGLRenderer({ alpha: true });
        cubeRenderer.setSize(300, 300);
        floatingCube.appendChild(cubeRenderer.domElement);
        
        cubeScene.add(cube);
        cubeCamera.position.z = 2;
        
        function animateCube() {
            requestAnimationFrame(animateCube);
            
            cube.rotation.x += 0.005;
            cube.rotation.y += 0.01;
            
            cubeRenderer.render(cubeScene, cubeCamera);
        }
        
        animateCube();
    }
    
    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        
        particlesMesh.rotation.x += 0.0005;
        particlesMesh.rotation.y += 0.0003;
        
        renderer.render(scene, camera);
    }
    
    animate();
    
    // Handle window resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

// Counter Animation
function initCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    
    if (counters.length === 0) return;
    
    const options = {
        rootMargin: '0px',
        threshold: 0.5
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-counter'));
                let count = 0;
                const duration = 2000; // 2 seconds
                const frameDuration = 1000 / 60; // 60fps
                const totalFrames = Math.round(duration / frameDuration);
                const increment = target / totalFrames;
                
                const timer = setInterval(() => {
                    count += increment;
                    counter.textContent = Math.floor(count);
                    
                    if (count >= target) {
                        counter.textContent = target;
                        clearInterval(timer);
                    }
                }, frameDuration);
                
                observer.unobserve(counter);
            }
        });
    }, options);
    
    counters.forEach(counter => {
        observer.observe(counter);
    });
}

// Testimonial Slider
function initTestimonialSlider() {
    const slider = document.getElementById('testimonial-slider');
    if (!slider) return;
    
    const slides = slider.querySelectorAll('.testimonial-slide');
    const prevBtn = document.getElementById('testimonial-prev');
    const nextBtn = document.getElementById('testimonial-next');
    
    let currentSlide = 0;
    
    // Show first slide initially
    slides[0].classList.add('active');
    
    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove('active'));
        
        if (index < 0) {
            currentSlide = slides.length - 1;
        } else if (index >= slides.length) {
            currentSlide = 0;
        } else {
            currentSlide = index;
        }
        
        slides[currentSlide].classList.add('active');
    }
    
    if (prevBtn && nextBtn) {
        prevBtn.addEventListener('click', () => {
            showSlide(currentSlide - 1);
        });
        
        nextBtn.addEventListener('click', () => {
            showSlide(currentSlide + 1);
        });
    }
    
    // Auto slideshow
    setInterval(() => {
        showSlide(currentSlide + 1);
    }, 5000);
}

// Glitch Effect
function initGlitchEffect() {
    const glitchTexts = document.querySelectorAll('.glitch-text');
    
    glitchTexts.forEach(text => {
        text.setAttribute('data-text', text.textContent);
    });
}

// Accordion
function initAccordions() {
    const accordionItems = document.querySelectorAll('.accordion-item');
    
    accordionItems.forEach(item => {
        const header = item.querySelector('.accordion-header');
        
        header.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Close all accordions
            accordionItems.forEach(accItem => {
                accItem.classList.remove('active');
            });
            
            // If the clicked one wasn't active, open it
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
} 