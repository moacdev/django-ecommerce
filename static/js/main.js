function app() {

    return {
        sideCart: false,
        cartLoading: true,
        orders: [],
        priceSum: 0,
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
                    console.log(JSON.parse(data.cart));
                    if (data.cart == null) {
                        return
                    }
                    this.orders = data.cart.orders
                    this.priceSum = data.priceSum
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

(function() {

})()