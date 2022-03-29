function app() {

    return {
        sideCart: false,
        cartLoading: true,
        cart: [],
        cartSum: 0,
        cartCount: 0,
        toggleSideCart() {
            if (this.sideCart == false) {
                this.fetchCart();
                this.sideCart = true;
            } else {
                this.sideCart = false;
            }
        },
        addToCart(productID) {
            const notyf = new window.Notyf()
                // loading

            const csrftoken = document.querySelector("div#csrf input[name='csrfmiddlewaretoken']").getAttribute("value")
            axios.defaults.headers.common['X-CSRFTOKEN'] = csrftoken;
            const config = {
                headers: {
                    'content-type': 'multipart/form-data'
                }
            }
            axios.post('/api/add-to-cart', { productID }).then(({
                data
            }) => {
                if (data.isOk) {
                    console.log("added");
                } else if (data.error_type == 'product-in-cart') {
                    notyf.error("Ce produit est déjà dans votre panier !")
                } else if (data.error_type == 'product-not-exist') {
                    notyf.error("Ce produit n'est plus disponble !")
                } else if (data.error_type == 'not-logged') {
                    window.location.href = "/connexion"
                } else {
                    notyf.error("Produit non ajouté au panier !")
                }
            }).catch(err => {
                console.log(err);
                notyf.error("Une erreur s'est produite durant l'ajout au panier.")
            }).finally(() => {
                // loading off
            })
        },
        fetchCart() {
            notyf = new window.Notyf()
            const csrftoken = document.querySelector("div#csrf input[name='csrfmiddlewaretoken']").getAttribute("value")
            axios.defaults.headers.common['X-CSRFTOKEN'] = csrftoken;
            this.cartLoading = true;
            axios.post("/api/get-cart").then(({
                data
            }) => {
                if (data.isOk) {
                    console.log(data.cart);
                    if (data.cart == null) {
                        return
                    }
                    this.cart = data.cart
                    this.cartSum = data.cartSum
                    this.cartCount = data.cartCount
                } else if (data.error_type == 'not-logged') {
                    window.location.href = "/connexion"
                } else {
                    notyf.error("Chargement du panier à échouer !")
                }
            }).catch(err => {
                console.log(err);
                notyf.error("Une erreur s'est produite durant le chargement du panier.")
            }).finally(() => {
                this.cartLoading = false;
            })
        },
    }
}



window.addEventListener('load', function() {

    function getGlideOptions(slideItems = 4){ 
        let perView = slideItems >= 4 ? 4 : slideItems
        let perView1200 = slideItems >= 3 ? 3 : slideItems
        let perView990 = slideItems >= 2 ? 2 : 1
        const options = {
            autoplay: 6000,
            perView,
            hoverpause: true,
            gap: 20,
            type: "carousel",
            breakpoints: {
                1200: {
                    perView: perView1200
                },
                990: {
                    perView: perView990
                },
                600: {
                    perView: 1
                }
            }
        }
        return options;
    }
    
    let new_products_el = document.querySelector('.glide-new-products')
    let new_products_length = new_products_el.getAttribute('pr-count')
    
    let new_product_loader = document.querySelector('#new-products-loader')

    let most_sold_products_el = document.querySelector('.glide-most-sold')
    let most_sold_products_length = most_sold_products_el.getAttribute('pr-count')
    let most_sold_loader = document.querySelector('#most-sold-loader')

    let most_popular_products_el = document.querySelector('.glide-most-popular')
    let most_popular_products_length = most_popular_products_el.getAttribute('pr-count')
    let most_popular_loader = document.querySelector('#most-popular-loader')
    

    let glide_new_products = new Glide(document.querySelector('.glide-new-products'), getGlideOptions(new_products_length)).mount()
    new_product_loader.classList.add('hidden')
    new_products_el.classList.remove('h-0')
    new_products_el.classList.remove('invisible')

    let glide_most_sold = new Glide(document.querySelector('.glide-most-sold'), getGlideOptions(most_sold_products_length)).mount()
    most_sold_loader.classList.add('hidden')
    most_sold_products_el.classList.remove('h-0')
    most_sold_products_el.classList.remove('invisible')

    let glide_most_popular = new Glide(document.querySelector('.glide-most-popular'), getGlideOptions(most_popular_products_length)).mount()
    most_popular_loader.classList.add('hidden')
    most_popular_products_el.classList.remove('h-0')
    most_popular_products_el.classList.remove('invisible')
})