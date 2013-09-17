sjcl.random.startCollectors();

var pshare = {
    random: function(n) {
        var words = []

        for (var i = 0; i < n; i++) {
            words.push(Math.random());
        }

        return words;
    },

    uniqueId: function(length) {
        if (!length) {
            length = 8;
        }

        var words = this.random(length);
        try {
            words = sjcl.random.randomWords(length);
        } catch (e) { /* This function can fail in Opera. :( */ }

        var id = this.hash(words);
        id = this.transform(id, length);
        return id.substr(0, length);
    },

    transform: function(data, length) {
        if (!length) {
            length = 8;
        }

        data = sjcl.codec.utf8String.toBits(data);
        data = sjcl.codec.base64.fromBits(data);
        data = data.replace(/[=]+$/, '');
        return data.substr(0, length);
    },

    hash: function(data) {
        return CryptoJS.RIPEMD160(data.toString());
    },

    createPad: function(id, password) {
        if (!id) {
            id = this.uniqueId(pshare.PRIVATE_ID_LENGTH);
        }
        if (!password) {
            password = this.uniqueId(pshare.PASSWORD_LENGTH);
        }

        id = this.hash(id);
        id = this.transform(id, pshare.PRIVATE_ID_LENGTH);

        password = this.hash(password);
        password = this.transform(password, pshare.PASSWORD_LENGTH);

        return {
            id: id,
            password: password
        };
    },

    encrypt: function(password, content) {
        return sjcl.encrypt(password, content);
    },

    decrypt: function(password, content) {
        return sjcl.decrypt(password, content);
    }
};

String.prototype.format = function() {
    var args = arguments;
    var str = this;

    return str.replace(String.prototype.format.regex, function(item) {
        var value = parseInt(item.substring(1, item.length - 1));
        if (value >= 0 && value < args.length) {
            return args[value];
        } else {
            return '';
        }
    });
};
String.prototype.format.regex = new RegExp('{-?[0-9]+}', 'g');
